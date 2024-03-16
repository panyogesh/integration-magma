import argparse
import subprocess
import yaml
from collections import namedtuple


## Execution sample
## python3.10 dictToYaml.py  --vxlanconfigfile=vxlanHostRed.yml --nscolor=red --nsip=192.168.60.13/16 --hostbridgeip=192.168.60.14/16 --vxlanid=100 --vxlanlocalip=192.168.60.11 --vxlanremoteip=192.168.60.12
#

NameSpaceConfig = namedtuple("NameSpaceConfig", ['color','ipaddr'])
HostMachineConfig = namedtuple("host_machine_config", ['bridgeip', 'vxlanid', 'vxlanlocalip', 'vxlanremoteip']) 
VxlanConfig = namedtuple('VxlanConfig', ['NameSpaceConfig', 'HostMachineConfig'])

class YamlUtils:
    def __init__(self, vxlanyamlconfigfile):
       self.ns_config         = None
       self.host_confg        = None
       self.vxlan_config      = None
       self.vxlan_yaml_config = vxlanyamlconfigfile 

    def create_vxlan_config_yaml(self, nscolor, nsip, hostbridgeip, vxlanid,
                                 vxlanlocalip, vxlanremoteip):
        vxlan_dict = {
            "namespace_config": {"nscolor": nscolor, "nsipaddr": nsip}, 
            "host_machine_config": {"ipaddrBridge": hostbridgeip, 
                             "vxlanid": vxlanid, "vxlanLocalIP": vxlanlocalip, 
                             "vxlanRemoteIP": vxlanremoteip}
            }

        with open(self.vxlan_yaml_config, "w") as file:
           # yaml.dump need a dict and a file handler as parameter
           yaml.dump(vxlan_dict, file)

    def _fetch_attribute(self, dictionary, attribute):
        if dictionary.get(attribute):
            value = dictionary.get(attribute)
        else:
            value = None

        if value is None:
            raise (yaml.YAMLError)

        return value

    def parse_vxlan_config_yaml(self) -> VxlanConfig:
        with open(self.vxlan_yaml_config) as stream:
            try:
                config_dict = yaml.safe_load(stream)
                if config_dict.get("namespace_config"):
                    namespace_config = config_dict.get("namespace_config")
                    nscolor = self._fetch_attribute(namespace_config, "nscolor")
                    nsipaddr = self._fetch_attribute(namespace_config, "nsipaddr")
                    self.ns_config = NameSpaceConfig(nscolor, nsipaddr)
               
                if config_dict.get("host_machine_config"):
                    host_machine_config = config_dict.get("host_machine_config")
                    bridge_ip = self._fetch_attribute(host_machine_config, "ipaddrBridge")
                    vxlan_id = self._fetch_attribute(host_machine_config, "vxlanid")
                    vxlan_local_ip = self._fetch_attribute(host_machine_config, "vxlanLocalIP")
                    vxlan_remote_ip = self._fetch_attribute(host_machine_config, "vxlanRemoteIP")
                    self.host_config = HostMachineConfig(bridge_ip, vxlan_id, vxlan_local_ip, vxlan_remote_ip) 
            
     
                self.vxlan_config = VxlanConfig(self.ns_config, self.host_config)

            except yaml.YAMLError as exc:
                print(exc)

        return self.vxlan_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vxlan Configuration creater / parser')
    parser.add_argument("--vxlanconfigfile", type=str, help="File to store generated conf")
    parser.add_argument("--nscolor", type=str, help="Color of namepace in host machine")
    parser.add_argument("--nsip", type=str, help="ip address of veth in namepace")
    parser.add_argument("--hostbridgeip", type=str, help="ip address of bridge in main namepace")
    parser.add_argument("--vxlanid", type=str, help="id of the vxlan")
    parser.add_argument("--vxlanlocalip", type=str, help="local-end ip in vlxan")
    parser.add_argument("--vxlanremoteip", type=str, help="remote-end ip in vlxan")

    args = parser.parse_args()
    yaml_utils = YamlUtils(args.vxlanconfigfile)
    yaml_utils.create_vxlan_config_yaml(args.nscolor, args.nsip,
                                        args.hostbridgeip, args.vxlanid,
                                        args.vxlanlocalip, args.vxlanremoteip)
    
    vxlan_config = yaml_utils.parse_vxlan_config_yaml()
    print(vxlan_config)
