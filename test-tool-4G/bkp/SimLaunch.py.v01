#!/usr/bin/python3.8

import sys
import pexpect
from pexpect import spawn, EOF
import ipaddress
import time
import socket
import psutil
from typing import NamedTuple, Tuple, Optional
import asyncio

class SIM_GNB_UE_PARAMS(NamedTuple):
    enb_local_ip_addr: str
    mme_remote_ip_addr: str
    imsi_id: str
    ue_key: str
    ue_opc: str
    mcc_mnc: str

class UtilManager:

    remote_machine_params=''
    rem_mac_password=''
    config_verify_cmd=''
    traffic_verify_cmd=''

    @classmethod
    def for_remote_excution_intialize(cls, rem_mac_ip, rem_mac_login="vagrant",
                                      rem_mac_password="vagrant"):

        # Store the password
        cls.rem_mac_password=rem_mac_password

        # Store the remote machine params
        cls.remote_machine_params="{}@{}".format(rem_mac_login, rem_mac_ip)
 
        # Update the Configuration verify command
        cls.config_verify_cmd="sudo ovs-ofctl dump-flows gtp_br0 table=13"

    @classmethod
    def get_ip_addresses(cls, family) -> str:

        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == family and snic.address != '127.0.0.1':
                    return (snic.address)
        return None

    @classmethod
    def validate_ip_address(cls, ip_string) -> bool:
        try:
           ip_object = ipaddress.ip_address(ip_string)
           return True
        except ValueError:
            print("The IP address '{ip_string}' is not valid")

        return False

    # Method to fetch the ipaddress of interface by tun name
    @classmethod
    def get_tun_ip_addresses(cls, family) -> str:
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if 'tun' in interface:
                   if snic.family == family and \
                      UtilManager.validate_ip_address(snic.address):
                    return (snic.address)
        return None

    # Method to fetch table-13 greped by tun ip address
    @classmethod
    def validate_config_entry_by_ipaddress(cls) -> bool:
        # Get the tunnel interface address
        tun_interface_ip = cls.get_tun_ip_addresses(socket.AF_INET)
        if tun_interface_ip is  None:
            print ("Failed in retriving tunnel IP address")
            return False;

        # Get the command to check if table=13 has the entries of configured IP
        rule_verify_cmd="{} | grep {} | wc -l".format(cls.config_verify_cmd, tun_interface_ip)

        # Run the command on remote machine
        command = [
          "sshpass", "-p", cls.rem_mac_password, "ssh", cls.remote_machine_params,
           rule_verify_cmd,
        ]

        output=subprocess.run(command, stdout=subprocess.PIPE, text=True)

        if "2" in output.stdout:
            print ("Rules Installed")
            return True

        print ("Fast Path Rules are not present")
        return False

class SimProcess(object):
    def __init__(self, create_child):
        self.child=create_child
        self.child.logfile_read=sys.stdout.buffer
        self.current_settings="0"
        self.s1ap_setup_cmd="15"
        self.attach_cmd="20"
        self.detach_cmd="21"
        self.setup_process_failure = 0
        self.attach_command_failure = 0
        self.detach_command_failure = 0
        self.tunnel_creation_failed = 0
        self.loop = asyncio.get_event_loop()

    def process_expect(self, match_str='Option:') -> bool: 
        try:
            self.child.expect(match_str, timeout=5)
            return True
        except pexpect.exceptions.EOF:
            print("EOF Reached")
        except pexpect.exceptions.TIMEOUT as pexpect_timeout:
            print("Timed out waiting for string {}".format(match_str))    

        return False

    def s1ap_setup_process(self) -> Tuple[int, int, int]:
        self.child.sendline(self.s1ap_setup_cmd)
        if (self.process_expect("S1AP: S1SetupResponse received") == False):
            self.setup_process_failure = self.setup_process_failure + 1
     
        return self.get_failure_information()

    async def tunnel_creation_status(self):
        if (UtilManager().validate_config_entry_by_ipaddress() == False):
            await asyncio.sleep(7)

        if (UtilManager().validate_config_entry_by_ipaddress() == False):
            self.tunnel_creation_failed = self.tunnel_creation_failed + 1

    def attach_command_process(self) -> Tuple[int, int, int]:
        self.child.sendline(self.attach_cmd)
        if (self.process_expect("NAS: EMMInformation received") == False):
            self.attach_command_failure = self.attach_command_failure + 1

        self.loop.create_task(self.tunnel_creation_status())
        return self.get_failure_information()

    def detach_command_process(self) -> Tuple[int, int, int]:
        self.child.sendline(self.detach_cmd)
        if (self.process_expect("NAS: DetachAccept received") == False):
            self.detach_command_failure = self.detach_command_failure + 1

        return self.get_failure_information()
    
    def get_failure_information(self) -> Tuple[int, int, int]:
        return (self.setup_process_failure, self.attach_command_failure,
                self.tunnel_creation_failed, self.detach_command_failure)

    def show_current_settings(self):
        self.process_expect()
        self.child.sendline(self.current_settings)

    def cleanup(self):
        self.child.close()
        sys.exit(self.child.status)


# Validate thte strings and return imsi and mcc_mnc strings 
def validate_parameters(sys) ->  Tuple[str, str]: 
    n=len(sys.argv)
    if n != 4:
        print(" Usage : {} <remote-mme-ip> <imsi> <mcc-mnc>".format(sys.argv[0]))
        exit()

    # Check whether MME IP is in correct format
    if (UtilManager.validate_ip_address(sys.argv[1]) == False):
        print("Validate the IP Address {}".format(sys.argv[1]))
        exit()

    # Store the details for verifying configuration on remote machines
    UtilManager.for_remote_excution_intialize(sys.argv[1])

    # Check if imsi length
    imsi_str=sys.argv[2]
    if len(imsi_str) != 15 or (imsi_str.isdigit() == False) :
        print(" IMSI should be 15 digits ")
        exit()

    mcc_mnc=sys.argv[3]
    if mcc_mnc.isdigit() == False:
        print("MCC-MNC is not in correct format")
        exit()
 
    return (imsi_str, mcc_mnc)

def excute_lte_call_flow(sys):
    (imsi_str, mcc_mnc) = validate_parameters(sys)

    key_str="465B5CE8B199B49FAA5F0A2EE238A6BC"
    opc_str="E8ED289DEBA952E4283B54E88E6183CA"

    config_params=SIM_GNB_UE_PARAMS(UtilManager.get_ip_addresses(socket.AF_INET), sys.argv[1],
                                imsi_str, key_str, opc_str, sys.argv[3])

    cmd="python3.8 ./eNB_LOCAL.py -i {} -m {} -I {} -K {} -C {} -o {}".format(
          config_params.enb_local_ip_addr, config_params.mme_remote_ip_addr,
          config_params.imsi_id, config_params.ue_key, config_params.ue_opc,
          config_params.mcc_mnc)

    print(cmd)
    
    sim_process=SimProcess(spawn(cmd, timeout=300))

    # Wait for the expect prompt
    sim_process.process_expect()

    # Start the s1setup procedure & Wait for Expect
    (setup_process_failure,_,_,_) = sim_process.s1ap_setup_process()
    if setup_process_failure:
        print("%% Failed to have setup procedure completed")
        exit()

    time.sleep(2)

    # Start the attach procedure & Wait for Expect
    (_, attach_command_failure, tunnel_creation_failed,_) = sim_process.attach_command_process()
    if attach_command_failure:
        print("%% Attach command failed")
        sim_process.cleanup()
        exit()

    if tunnel_creation_failed:
        print("%% Tunnel creation failed")

    time.sleep(3)

    # Start the detach procedure & Wait for Expect
    (_,_,_,detach_command_failure) = sim_process.detach_command_process()
    if detach_command_failure:
        print("%% Detach command failed")

    time.sleep(2)
    sim_process.cleanup()

if __name__ == '__main__':
   excute_lte_call_flow(sys) 
