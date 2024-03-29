#!/usr/bin/python3.8

""" Module creating client profiles for 4G eNB/UE Simulator server """
import argparse
import os
import sys
import ipaddress
import time
import socket
import subprocess
import select
import logging
import random
from typing import (
    NamedTuple)
import netifaces

# Tuple for configuration parameters
# Remote machine parameters


class DUTMachineParams(NamedTuple):
    """ A NamedTuple class to store DUT machine parameters """
    mme_remote_ip_addr: str
    username: str
    password: str


class SimGNBUEParams(NamedTuple):
    """ A NamedTuple to store all parameters passed for Client/Server """
    enb_local_ip_addr: str
    imsi_id: str
    ue_key: str
    ue_opc: str
    mcc_mnc: str
    connected_loop: bool
    dut_params: NamedTuple("DUTMachineParams",
                           [('mme_remote_ip_addr', str), ('username', str),
                            ('password', str)])

# Utility class for related actions
class UtilManager:
    """ Class for common utility functionality """
    logger = logging.getLogger()

    # For getting the ip address of the interface
    # This interface gets connected to mme
    @classmethod
    def get_ip_addresses(cls, family) -> str:
        """ Get the first no-lo ip address for docker """
        for iface in netifaces.interfaces():
            if iface == 'lo' or 'tun' in iface:
                continue

            if family == socket.AF_INET:
                iface_details = netifaces.ifaddresses(iface)
                if iface_details[netifaces.AF_INET]:
                    return iface_details[netifaces.AF_INET][0]['addr']

        return None

    # Util: For validating the ip address
    @classmethod
    def validate_ip_address(cls, ip_string) -> bool:
        """ Validate the ip address passed as part of arguments """
        try:
            ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            cls.logger.error("The IP address '{ip_string}' is not valid")

        return False

# Seperate class for configuration validation
class ConfigValidator:
    """ Class for checking the configured OVS rules from DUT"""
    config_verify_cmd = 'sudo ovs-ofctl dump-flows gtp_br0 table=13'
    logger = logging.getLogger()

    @classmethod
    def update_dut_params(cls, dut_params):
        """ Store the dut parameters for config validation """
        cls.dut_params = dut_params

    # Method to fetch the ipaddress of interface by tun name
    @classmethod
    def get_tun_ip_addresses(cls, family, tun_name: str) -> str:
        """ Fetch the tunnel ip address by tunnel name """
        iface_details = netifaces.ifaddresses(tun_name)

        if family in iface_details and \
           family == netifaces.AF_INET and \
           iface_details[netifaces.AF_INET][0]:
            ipv4_addr = iface_details[netifaces.AF_INET][0]['addr']
            return ipv4_addr

        return None

    @classmethod
    def get_ue_rules_from_dut(cls, imsi_str: str):
        """ Get the ue rules from DUT Machine """
        tun_name = "tun"+str((int(imsi_str[-4:]) + 10000))
        if tun_name not in netifaces.interfaces():
            return False

        # Fetch the tunnel ip address
        tun_interface_ip = cls.get_tun_ip_addresses(socket.AF_INET, tun_name)
        if tun_interface_ip is None:
            cls.logger.error("Failed in retriving tunnel IP address")
            return False

        return True

# Class for simulating client process
class SimProcess():
    """ Class for client process,that interacts with server"""
    def __init__(self, server_detail, imsi_id):
        self.server_info = server_detail + imsi_id
        self.imsi_str = imsi_id
        self.client_sock = 0
        self.socket_buffer = 1024
        self.logger = logging.getLogger()
        self.list_msg = []

        self.cmd_db = {
            # Show current settings
            'CURRENT_SETTINGS_CMD':
            {'CMD_ID': '0', 'FailStats': 0},

            # S1AP Setup entry
            'S1AP_SETUP_CMD':
            {'CMD_ID': '15\n', 'FailStats': 0,
             'MATCH_RESP': 'S1AP: S1SetupResponse received'},

            # S1AP RESET entry
            'S1AP_RESET_CMD':
            {'CMD_ID': '16\n', 'FailStats': 0,
             'MATCH_RESP': 'S1AP: S1AP: ResetAcknowledge received'},

            # Attach command entry
            'ATTACH_CMD':
            {'CMD_ID': '20\n', 'FailStats': 0,
             'MATCH_RESP': 'NAS: EMMInformation received'},

            # Detach command entry
            'DETACH_CMD':
            {'CMD_ID': '21\n', 'FailStats': 0,
             'MATCH_RESP': 'NAS: DetachAccept received'},

            # Service request entry
            'SERVICE_REQUEST':
            {'CMD_ID': '24\n', 'FailStats': 0,
             'MATCH_RESP': 'S1AP: sending InitialContextSetupResponse'},

            # Release ue context entry
            'RELEASE_UE_CTXT_CMD':
            {'CMD_ID': '25\n', 'FailStats': 0,
             'MATCH_RESP': 'S1AP: sending UEContextReleaseComplete'},

            # Activate GTPU IP entry
            'ACTIVATE_GTPU_IP':
            {'CMD_ID': '50\n', 'FailStats': 0,
             'MATCH_RESP': 'GTP-U/IP over ControlPlane: Activation'},

            # Deactivate GTPU IP entry
            'DEACTIVATE_GTPU_IP':
            {'CMD_ID': '51\n', 'FailStats': 0,
             'MATCH_RESP': 'GTP-U/IP over ControlPlane: Desactivation'},

            # Cler log command
            'CLEAR_LOG_CMD':
            {'CMD_ID': '99\n', 'FailStats': 0},

            # Quit the eNB and UE simulator
            'QUIT_CMD':
            {'CMD_ID': 'Q\n', 'FailStats': 0},

            # Additional verification commands

            # Datapath command
            'TUNNEL_DATAPATH_CMD': {'FailStats': 0}
        }

    # Connect to FassFeraz server
    def connect_to_server(self, imsi_port: int):
        """ Initiate connection to server """
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(("127.0.0.1", 50001 +imsi_port))

    # For expect handling
    def read_server_response(self, match_str) -> bool:
        """ Read the respoonse from server """
        while True:

            # Wait for 45 seconds to timeout
            read_socket, _, _ =\
                select.select([self.client_sock], [], [], 45)

            # Timeout reached return fails
            if not read_socket:
                break

            # Read messages if the socket is in read_socket
            if self.client_sock in read_socket:
                msg_from_server =\
                    self.client_sock.recv(self.socket_buffer)

                # Append the messages in list_msg
                self.list_msg.append(msg_from_server.decode())

                # If this is the exected message reutrn in less then 2 attempts
                # and within timeout of 45 seconds each return
                if msg_from_server.decode() == match_str:
                    return True

        return False

    # For clearing the logs
    def clear_logs(self):
        """ Function to clear locally stored logs """
        self.list_msg.clear()

    # Increment failure
    def increment_fail_stats(self, exec_cmd: str):
        """ Increment failed stats for debugging purpose """
        if exec_cmd in self.cmd_db.keys():
            self.cmd_db[exec_cmd]['FailStats'] += 1

    # Establish the connection with server
    def setup_connection_with_server(self, imsi_port: int):
        """" Attemt connection with server """

        # Attempt connection 10 times with a delay of second
        conn_attempt = 0
        while conn_attempt < 100:
            try:
                self.connect_to_server(imsi_port)
                return True
            except ConnectionResetError:
                conn_attempt += 1
                time.sleep(1)
            except ConnectionRefusedError:
                conn_attempt += 1
                time.sleep(1)

        return False

    # Execute the command in fassferraz
    def send_command_to_server(self, cmd_str: str) -> bool:
        """ Send command to server for initiating message towards EPC"""

        self.logger.debug("Executing : %s", cmd_str)
        cmd_to_server = str.encode(self.cmd_db.get(cmd_str).get('CMD_ID'))

        if cmd_str in ['QUIT_CMD', 'CLEAR_LOG_CMD']:
            try:
                self.client_sock.sendall(cmd_to_server)
            except OSError:
                self.logger.error(
                    " Bad File descriptor %s", cmd_to_server)
                return False
        else:
            try:
                self.client_sock.sendall(cmd_to_server)
            except OSError:
                self.logger.error(
                    " Bad File descriptor %s", cmd_to_server)
                return False

            if self.read_server_response(
                    self.cmd_db.get(cmd_str).get('MATCH_RESP')):
                return True

        self.increment_fail_stats(cmd_str)
        return False

    # Verify tunnel datapath
    def verify_tunnel_data_path(self):
        """ Function to verify if tunnel is configured on DUT """
        return ConfigValidator.get_ue_rules_from_dut(self.imsi_str)

    # S1AP_SETUP_CMD : For setup request
    def s1ap_setup_process(self) -> bool:
        """ Send s1ap setup request to EPC from server """
        return self.send_command_to_server('S1AP_SETUP_CMD')

    # For reseting the S1AP Connection
    def s1ap_reset_request(self) -> bool:
        """ Send s1ap reset request to EPC from server """
        return self.send_command_to_server('S1AP_RESET_CMD')

    # ATTACH_CMD : For attach command
    def attach_command_process(self) -> bool:
        """ Send attach command to EPC from server """
        return self.send_command_to_server('ATTACH_CMD')

    # DETACH_CMD : For detach command
    def detach_command_process(self) -> bool:
        """ Send detach command to EPC from server """
        return self.send_command_to_server('DETACH_CMD')

    # RELEASE_UE_CTXT_CMD : For releasing the ue context
    def release_ue_context_command_process(self) -> bool:
        """ Send release ue context to EPC from server """
        return self.send_command_to_server('RELEASE_UE_CTXT_CMD')

    # For service request command
    def service_request_command_process(self) -> bool:
        """ Send service request command to EPC from server """
        return self.send_command_to_server('SERVICE_REQUEST')

    # For Activate GTPU IP command
    def activate_gtpu_ip_command_process(self) -> bool:
        """ Activate gtpu ip configuration on local system """
        return self.send_command_to_server('ACTIVATE_GTPU_IP')

    # For Deactivate GTPU IP command
    def deactivate_gtpu_ip_command_process(self) -> bool:
        """ Deactivate gtpu ip configuration on local system """
        return self.send_command_to_server('DEACTIVATE_GTPU_IP')

    def show_current_settings(self):
        """ Ask Server to show all configuration options """
        self.read_server_response(None)
        # self.child.sendline(self.current_settings)

    def cleanup(self):
        """ Clean up once all operations are done. Stop the server  """
        self.logger.error('\nMessage entries : %s', '\n -> '.
                          join(entries for entries in self.list_msg))
        self.logger.error(" Clean up called ")
        self.send_command_to_server('QUIT_CMD')

# Loop for connected request


def service_connect_loop(sim_process: SimProcess):
    """ Function for calling service connect in loop """
    if not sim_process.deactivate_gtpu_ip_command_process():
        sim_process.logger.error("%% Failed in deactivating gtpu ")
        sim_process.cleanup()
        return False

    time.sleep(1)
    if not sim_process.release_ue_context_command_process():
        sim_process.logger.error("%% Failed to release ue context")
        return False

    time.sleep(1)
    if not sim_process.service_request_command_process():
        sim_process.logger.error("%% Failed to send service request command")
        return False

    time.sleep(1)
    if not sim_process.activate_gtpu_ip_command_process():
        sim_process.logger.error("%% Failed in activating gtpu ip")
        return False

    time.sleep(1)
    if not sim_process.verify_tunnel_data_path():
        sim_process.logger.error("%% Traffic Tests are not through")
        # sim_process.cleanup()

    time.sleep(1)
    return True

# Loop for attach and service request
def attach_process_in_loop(sim_process: SimProcess, connected_loop: bool):
    """ Iteration for attach and service request """
    attach_iteration = 1
    service_request_iteration = 1
    time_interval = 1

    if connected_loop:
        attach_iteration = 1000
        service_request_iteration = 5
        time_interval = 60

    while attach_iteration:
        # Start the attach procedure & Wait for Expect
        if not sim_process.attach_command_process():
            sim_process.logger.error("%% Attach command failed")
            return False

        time.sleep(random.randint(80, 180))

        # Start the detach procedure & Wait for Expect
        if not sim_process.detach_command_process():
            sim_process.logger.error("%% Detach command failed")
            if not sim_process.s1ap_reset_request():
                sim_process.logger.error("%% S1AP Reset also failed")

        attach_iteration -= 1
        sim_process.logger.info(
                " --- Looping %d attach_iteration ---", attach_iteration)
        time.sleep(time_interval)


# Loop for attach and service request
def service_request_process_in_loop(sim_process: SimProcess, connected_loop: bool):
    """ Iteration for attach and service request """
    attach_iteration = 1
    service_request_iteration = 1
    time_interval = 1

    if connected_loop:
        attach_iteration = 2
        service_request_iteration = 2
        time_interval = 10

    while attach_iteration:
        # Start the attach procedure & Wait for Expect
        if not sim_process.attach_command_process():
            sim_process.logger.error("%% Attach command failed")
            return False

        time.sleep(1)

        if not sim_process.activate_gtpu_ip_command_process():
            sim_process.logger.error("%% Failed in activating gtpu ip")
            return False

        time.sleep(1)
        if not sim_process.verify_tunnel_data_path():
            sim_process.logger.error("%% Traffic Tests are not through")

        while service_request_iteration:
            if not service_connect_loop(sim_process):
                sim_process.logger.error(
                    "%% Failed service request at %d iteration",
                    service_request_iteration)
                break

            service_request_iteration -= 1
            sim_process.logger.info(
                " --- Looping %d service_request_iteration ---",
                service_request_iteration)
            time.sleep(time_interval)

        # Start the detach procedure & Wait for Expect
        if not sim_process.detach_command_process():
            sim_process.logger.error("%% Detach command failed")
            if not sim_process.s1ap_reset_request():
                sim_process.logger.error("%% S1AP Reset also failed")

        attach_iteration -= 1
        sim_process.logger.info(
                " --- Looping %d attach_iteration ---", attach_iteration)
        time.sleep(time_interval)

# Launch the client process
def launch_client(imsi_id: str, connected_loop: bool) -> bool:
    """ Launch the client and connect with FassFerraz server """
    sim_process = SimProcess("FasFerraz-Client", imsi_id)

    if not sim_process.setup_connection_with_server(int(imsi_id[-4:])):
        sim_process.logger.error("%% Failed to setup connection with server")
        return False

    # Start the s1setup procedure & Wait for Expect
    if not sim_process.s1ap_setup_process():
        sim_process.logger.error("%% Failed to have setup procedure completed")
        return False


    attach_process_in_loop(sim_process, connected_loop)

    sim_process.cleanup()
    return True

# Validate thte strings and return imsi and mcc_mnc strings


def update_sim_dut_params(args) -> SimGNBUEParams:
    """ Validate and store the DUT related parameters """
    # Check whether MME IP is in correct format
    if not UtilManager.validate_ip_address(args.mme_ip):
        print("Validate the mme IP Address {}".format(args.mme_ip))
        sys.exit()

    # Check whether ENB LOCAL IP is in correct format
    if args.enb_ip and \
       not UtilManager.validate_ip_address(args.enb_ip):
        print("Validate the local IP Address {}".format(args.enb_ip))
        sys.exit()

    # Check if imsi length
    if len(args.imsi) != 15 or (not args.imsi.isdigit()):
        print(" IMSI should be 15 digits ")
        sys.exit()

    # Check format of mcc-mnc
    if not args.mcc_mnc.isdigit():
        print("MCC-MNC is not in correct format")
        sys.exit()

    # Do we need connected loop test
    if args.connected_loop:
        connected_loop = args.connected_loop
    else:
        connected_loop = False

    # Dut login parameters
    if args.dut_login:
        login = args.username
    else:
        login = 'vagrant'

    # Dut login password
    if args.dut_passwd:
        password = args.dut_passwd
    else:
        password = 'vagrant'

    key_str = "465B5CE8B199B49FAA5F0A2EE238A6BC"
    opc_str = "E8ED289DEBA952E4283B54E88E6183CA"

    dut_params = DUTMachineParams(args.mme_ip, login, password)

    ConfigValidator.update_dut_params(dut_params)

    if args.enb_ip:
        local_ip = args.enb_ip
    else:
        local_ip = UtilManager.get_ip_addresses(socket.AF_INET)

    return SimGNBUEParams(local_ip, args.imsi, key_str, opc_str,
                          args.mcc_mnc, connected_loop, dut_params)


def excute_lte_call_flow(conf_params: SimGNBUEParams):
    """ Main starter function. Launches server and then client """
    server_launch_cmd =\
        "python3.8 ./eNB_LOCAL.py -i {} -m {} -I {} -K {} -C {} -o {}".format(
            conf_params.enb_local_ip_addr,
            conf_params.dut_params.mme_remote_ip_addr,
            conf_params.imsi_id, conf_params.ue_key, conf_params.ue_opc,
            conf_params.mcc_mnc)

    # Launching server
    sim_proc_id = subprocess.Popen(server_launch_cmd.split(),
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.PIPE)

    print(server_launch_cmd)

    time.sleep(1)

    # Launching client
    launch_client(conf_params.imsi_id, conf_params.connected_loop)

    try:
        os.waitpid(sim_proc_id.pid, 0)
    except ChildProcessError:
        print(" Child process cleanly sys.exited ")
    except Exception as ex: # pylint:disable=broad-except
        res = sim_proc_id.communicate()
        print(ex)
        print("retcode = ", sim_proc_id.returncode, file=sys.stderr)
        print("res=", res, file=sys.stderr)


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser()

    PARSER.add_argument('--mme_ip', type=str, help="MME/DUT IP to connect",
                        required=True)

    PARSER.add_argument('--imsi', type=str, help="IMSI or Subscriber identifier",
                        required=True)

    PARSER.add_argument('--mcc_mnc', type=str, help="MCC and MNC of operator",
                        required=True)

    PARSER.add_argument('--enb_ip', type=str,
                        help="Local enb ip to connect to mme")

    PARSER.add_argument('--dut_login', type=str,
                        help="username of dut machine")

    PARSER.add_argument('--dut_passwd', type=str,
                        help="password of dut machine")

    PARSER.add_argument('--connected_loop', type=bool, default=False)

    ARGUMENTS = PARSER.parse_args()

    LOG_FILE_NAME = os.path.join(os.environ['LOGPATH'],
                            "simprocess_{}.log".format(ARGUMENTS.imsi[-4:]))

    logging.basicConfig(
        filename=LOG_FILE_NAME,
        level=logging.DEBUG,
        format='[%(asctime)s %(levelname)s %(name)s %(funcName)s] %(message)s',
    )

    CONFIG_PARAMS = update_sim_dut_params(ARGUMENTS)

    excute_lte_call_flow(CONFIG_PARAMS)
