#!/usr/bin/python3.8

import argparse
import os
import sys
import pexpect
from pexpect import spawn, EOF
import ipaddress
import time
import socket
import netifaces 
from typing import NamedTuple, Tuple, Optional
import asyncio
from enum import Enum
import subprocess
import logging
import paramiko
import select

# Tuple for configuration parameters
# Remote machine parameters
class DUTMachineParams(NamedTuple):
    mme_remote_ip_addr: str
    username: str
    password: str

class SimGNBUEParams(NamedTuple):
    enb_local_ip_addr: str
    imsi_id: str
    ue_key: str
    ue_opc: str
    mcc_mnc: str
    dut_params: NamedTuple("DUTMachineParams",
                          [('mme_remote_ip_addr', str), ('username', str),
                           ('password', str)])

# Utility class for related actions
class UtilManager:

    logger = logging.getLogger()

    # For getting the ip address of the interface
    # This interface gets connected to mme
    @classmethod
    def get_ip_addresses(cls, family) -> str:
        for iface in netifaces.interfaces():
            if iface == 'lo':
                continue

            iface_details = netifaces.ifaddresses(iface)
            if iface_details[netifaces.AF_INET]:
                return iface_details[netifaces.AF_INET][0]['addr']
        return None

    # Util: For validating the ip address
    @classmethod
    def validate_ip_address(cls, ip_string) -> bool:
        try:
           ip_object = ipaddress.ip_address(ip_string)
           return True
        except ValueError:
            cls.logger.error("The IP address '{ip_string}' is not valid")

        return False

# Seperate class for configuration validation
class ConfigValidator:
    config_verify_cmd='sudo ovs-ofctl dump-flows gtp_br0 table=13'
    logger = logging.getLogger()

    @classmethod
    def update_dut_params(cls, dut_params):
        cls.dut_params= dut_params

    # Method to fetch the ipaddress of interface by tun name
    @classmethod
    def get_tun_ip_addresses(cls, family, tun_name: str) -> str:
        iface_details = netifaces.ifaddresses(tun_name)
        
        if family in iface_details and \
           family == netifaces.AF_INET and \
           iface_details[netifaces.AF_INET][0]:
            ip = iface_details[netifaces.AF_INET][0]['addr']
            return ip

        return None    

    @classmethod
    def get_ue_rules_from_dut(cls, imsi_str: str):
        tun_name="tun"+str((int(imsi_str[-4:]) + 10000))
        if tun_name not in netifaces.interfaces():
            return False

        # Fetch the tunnel ip address
        tun_interface_ip = cls.get_tun_ip_addresses(socket.AF_INET, tun_name)
        if tun_interface_ip is  None:
            cls.logger.error("Failed in retriving tunnel IP address")
            return False

        return True
'''
        table_string=\
          "sudo ovs-ofctl dump-flows gtp_br0 table=13 | grep {}".format(
          tun_interface_ip)

        # Get the command to check if table=13 has the entries of configured IP
        cmd='"--mme_ip {}""  "--exec_command {}"'.format(
             cls.dut_params.mme_remote_ip_addr, table_string)

        dut_process=\
          subprocess.Popen(["python3.8", "./dutcmdexec.py",
                            "--mme_ip", cls.dut_params.mme_remote_ip_addr,
                            "--exec_command", table_string],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

        try:    
            stdout, stderr = dut_process.communicate()
        except:
            cls.logger.error(" %% Not able execute remote command")

        cls.logger.info(stdout)

        return stdout 
'''

# Class for simulating client process
class SimProcess(object):

    def __init__(self, server_detail, imsi_id):
        self.server_info=server_detail + imsi_id
        self.imsi_str = imsi_id
        self.client_sock=0
        self.socket_buffer=1024
        self.logger = logging.getLogger()
        self.list_msg = [] 

        self.cmd_db = {
            # Show current settings
            'CURRENT_SETTINGS_CMD':
               {'CMD_ID' : '0', 'FailStats' : 0},

            # S1AP Setup entry
            'S1AP_SETUP_CMD':
               {'CMD_ID' : '15\n', 'FailStats' : 0,
                'MATCH_RESP': 'S1AP: S1SetupResponse received'},

            # S1AP RESET entry
            'S1AP_RESET_CMD':
               {'CMD_ID' : '16\n', 'FailStats' : 0,
                'MATCH_RESP': 'S1AP: S1AP: ResetAcknowledge received'},

            # Attach command entry
            'ATTACH_CMD':
               {'CMD_ID' : '20\n', 'FailStats' : 0,
                'MATCH_RESP': 'NAS: EMMInformation received'},

            # Detach command entry
            'DETACH_CMD':
               {'CMD_ID' : '21\n', 'FailStats' : 0,
                'MATCH_RESP': 'NAS: DetachAccept received'},

            # Service request entry
            'SERVICE_REQUEST':
               {'CMD_ID' : '24\n', 'FailStats' : 0,
                'MATCH_RESP': 'S1AP: sending InitialContextSetupResponse'},

            # Release ue context entry
            'RELEASE_UE_CTXT_CMD':
               {'CMD_ID' : '25\n', 'FailStats' : 0,
                'MATCH_RESP' : 'S1AP: sending UEContextReleaseComplete'},

            # Activate GTPU IP entry
            'ACTIVATE_GTPU_IP':
               {'CMD_ID' : '50\n', 'FailStats' : 0,
                'MATCH_RESP' : 'GTP-U/IP over ControlPlane: Activation'},

            # Deactivate GTPU IP entry
            'DEACTIVATE_GTPU_IP':
               {'CMD_ID' : '51\n', 'FailStats' : 0,
                'MATCH_RESP' : 'GTP-U/IP over ControlPlane: Desactivation'},

            # Cler log command
            'CLEAR_LOG_CMD':
               {'CMD_ID' : '99\n', 'FailStats' : 0},

            # Quit the eNB and UE simulator
            'QUIT_CMD':
               {'CMD_ID' : 'Q\n'},

            # Additional verification commands

            # Datapath command 
            'TUNNEL_DATAPATH_CMD': {'FailStats' : 0}
        }

    # Connect to FassFeraz server
    def connect_to_server(self):
        self.client_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(("127.0.0.1", 65432))

    # For expect handling
    def read_server_response(self, match_str) -> bool:
       
        while True:

            # Wait for 45 seconds to timeout
            read_socket, _, _ =\
                select.select([self.client_sock], [], [], 45)

            # Timeout reached return fails
            if not read_socket:
                break

            # Read messages if the socket is in read_socket
            if self.client_sock in read_socket:
                msg_from_server=\
                    self.client_sock.recv(self.socket_buffer)
           
                self.logger.error(msg_from_server.decode())

                # Append the messages in list_msg      
                self.list_msg.append(msg_from_server.decode())

                # If this is the exected message reutrn in less then 2 attempts
                # and within timeout of 45 seconds each return
                if (msg_from_server.decode() == match_str):
                    return True

        return False

    # For clearing the logs
    def clear_logs(self):
        self.list_msg.clear()

    # Increment failure
    def increment_fail_stats(self, exec_cmd: str):
        if exec_cmd in self.cmd_db.keys():
            self.cmd_db[exec_cmd]['FailStats']+=1

    # Establish the connection with server
    def setup_connection_with_server(self):
        # Attempt connection 10 times with a delay of second
        conn_attempt=0
        while conn_attempt < 100:
            try:
                self.connect_to_server()
                return True
            except ConnectionResetError:
                conn_attempt+=1
                time.sleep(1)
            except ConnectionRefusedError:
                conn_attempt+=1
                time.sleep(1)

        return False

    # Execute the command in fassferraz
    def send_command_to_server(self, cmd_str: str) -> bool:
        #self.child.sendline(self.cmd_db.get(cmd_str).get('CMD_ID'))

        self.logger.debug("Executing : {}".format(cmd_str))
        cmd_to_server=str.encode(self.cmd_db.get(cmd_str).get('CMD_ID'))
       
        if cmd_str in ['QUIT_CMD', 'CLEAR_LOG_CMD']:
            self.client_sock.sendall(cmd_to_server)
            self.client_sock.close()
        else:    
            self.client_sock.sendall(cmd_to_server)
            if (self.read_server_response(
                self.cmd_db.get(cmd_str).get('MATCH_RESP')) == False):
                self.increment_fail_stats(cmd_str)
                return False

        return True

    #Verify tunnel datapath
    def verify_tunnel_data_path(self):
        return (ConfigValidator.get_ue_rules_from_dut(self.imsi_str))

    # S1AP_SETUP_CMD : For setup request
    def s1ap_setup_process(self) -> bool:
        return (self.send_command_to_server('S1AP_SETUP_CMD'))

    # For reseting the S1AP Connection
    def s1ap_reset_request(self) -> bool:
        return (self.send_command_to_server('S1AP_RESET_CMD'))

    # ATTACH_CMD : For attach command
    def attach_command_process(self) -> bool:
        return (self.send_command_to_server('ATTACH_CMD'))

    # DETACH_CMD : For detach command
    def detach_command_process(self) -> bool:
        return (self.send_command_to_server('DETACH_CMD'))

    # RELEASE_UE_CTXT_CMD : For releasing the ue context
    def release_ue_context_command_process(self) -> bool:
        return (self.send_command_to_server('RELEASE_UE_CTXT_CMD'))

    # For service request command 
    def service_request_command_process(self) -> bool:
        return (self.send_command_to_server('SERVICE_REQUEST'))

    # For Activate GTPU IP command
    def activate_gtpu_ip_command_process(self) -> bool:
        return (self.send_command_to_server('ACTIVATE_GTPU_IP'))

    # For Deactivate GTPU IP command
    def deactivate_gtpu_ip_command_process(self) -> bool:
        return (self.send_command_to_server('DEACTIVATE_GTPU_IP'))

    def show_current_settings(self):
        self.read_server_response()
        #self.child.sendline(self.current_settings)

    def cleanup(self):
        self.logger.info('Message entries : %s', '\n -> '.
                         join(entries for entries in self.list_msg))
        self.logger.debug(" Clean up called ") 
        self.send_command_to_server('QUIT_CMD')

# Launch the client process
def launch_client(imsi_id: str):
    #sim_process=SimProcess(spawn(cmd, timeout=300))
    sim_process=SimProcess("FasFerraz-Client", imsi_id)

    if (sim_process.setup_connection_with_server() == False):
        sim_process.logger.error("%% Failed to setup connection with server")
        return

    # Start the s1setup procedure & Wait for Expect
    if (sim_process.s1ap_setup_process() == False):
        sim_process.logger.error("%% Failed to have setup procedure completed")
        return False

    # Start the attach procedure & Wait for Expect
    if (sim_process.attach_command_process() == False):
        sim_process.logger.error("%% Attach command failed")
        sim_process.cleanup()
        return False

    time.sleep(1)

    if (sim_process.activate_gtpu_ip_command_process() == False):
        sim_process.logger.error("%% Failed in activating gtpu ip")
        sim_process.cleanup()
        return False

    time.sleep(1)
    if (sim_process.verify_tunnel_data_path() == False):
        sim_process.logger.error("%% Traffic Tests are not through")
        #sim_process.cleanup()
        #return False


    time.sleep(1)
    if (sim_process.deactivate_gtpu_ip_command_process() == False):
        sim_process.logger.error("%% Failed in deactivating gtpu ")
        sim_process.cleanup()
        return False

    time.sleep(1)
    if (sim_process.release_ue_context_command_process() == False):
        sim_process.logger.error("%% Failed to release ue context")
        sim_process.cleanup()
        return False

    time.sleep(1)
    if (sim_process.service_request_command_process() == False):
        sim_process.logger.error("%% Failed to send service request command")
        sim_process.cleanup()
        return False

    time.sleep(1)
    if (sim_process.activate_gtpu_ip_command_process() == False):
        sim_process.logger.error("%% Failed in activating gtpu ip")
        sim_process.cleanup()
        return False

    time.sleep(1)
    if (sim_process.verify_tunnel_data_path() == False):
        sim_process.logger.error("%% Traffic Tests are not through")
        #sim_process.cleanup()

    time.sleep(1)

    # Start the detach procedure & Wait for Expect
    if (sim_process.detach_command_process() == False):
        sim_process.logger.error("%% Detach command failed")
        if (sim_process.s1ap_reset_request() == False):
            sim_process.logger.error("%% S1AP Reset also failed")

    sim_process.cleanup()
    return True

# Validate thte strings and return imsi and mcc_mnc strings
def update_sim_dut_params(arguments) -> SimGNBUEParams:

    # Check whether MME IP is in correct format
    if (UtilManager.validate_ip_address(arguments.mme_ip) == False):
        print("Validate the mme IP Address {}".format(arguments.mme_ip))
        exit()

    # Check whether ENB LOCAL IP is in correct format
    if arguments.enb_ip and \
       UtilManager.validate_ip_address(arguments.enb_ip) == False:
        print("Validate the local IP Address {}".format(arguments.enb_ip))
        exit()

    # Check if imsi length
    if len(arguments.imsi) != 15 or (arguments.imsi.isdigit() == False) :
        print(" IMSI should be 15 digits ")
        exit()

    # Check format of mcc-mnc
    if arguments.mcc_mnc.isdigit() == False:
        print("MCC-MNC is not in correct format")
        exit()

    if arguments.dut_login:
       login=arguments.username
    else:
       login='vagrant'

    if arguments.dut_passwd:
       password=arguments.dut_passwd
    else:
       password='vagrant'

    key_str="465B5CE8B199B49FAA5F0A2EE238A6BC"
    opc_str="E8ED289DEBA952E4283B54E88E6183CA"

    dut_params=DUTMachineParams(arguments.mme_ip, login, password)

    ConfigValidator.update_dut_params(dut_params)

    if arguments.enb_ip:
        local_ip = arguments.enb_ip
    else:
        local_ip = UtilManager.get_ip_addresses(socket.AF_INET)

    return SimGNBUEParams(local_ip, arguments.imsi, key_str, opc_str,
                          arguments.mcc_mnc, dut_params)

def excute_lte_call_flow(sys):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--mme_ip', type=str, help="MME/DUT IP to connect",
                        required=True)
    
    parser.add_argument('--imsi', type=str, help="IMSI or Subscriber identifier",
                        required=True)
    
    parser.add_argument('--mcc_mnc', type=str, help="MCC and MNC of operator",
                        required=True)

    parser.add_argument('--enb_ip', type=str, help="Local enb ip to connect to mme")

    parser.add_argument('--dut_login', type=str,
                        help="username of dut machine")
    
    parser.add_argument('--dut_passwd', type=str, help="password of dut machine")

    arguments = parser.parse_args() 

    config_params=update_sim_dut_params(arguments)

    server_launch_cmd=\
         "python3.8 ./eNB_LOCAL.py -i {} -m {} -I {} -K {} -C {} -o {}".format(
         config_params.enb_local_ip_addr,
         config_params.dut_params.mme_remote_ip_addr,
         config_params.imsi_id, config_params.ue_key, config_params.ue_opc,
         config_params.mcc_mnc)

    #Launching server      
    sim_proc_id=0
    sim_proc_id=subprocess.Popen(server_launch_cmd.split()).pid
    print(server_launch_cmd)

    time.sleep(1)

    #Launching client 
    launch_client(config_params.imsi_id)

    try:
        pid, status = os.waitpid(sim_proc_id, 0)
    except ChildProcessError:
        print(" Child process cleanly exited ")


if __name__ == '__main__':
   logging.basicConfig(
       filename="simprocess.log",
       level=logging.DEBUG,
       format='[%(asctime)s %(levelname)s %(name)s %(funcName)s] %(message)s',
    )

   excute_lte_call_flow(sys) 
