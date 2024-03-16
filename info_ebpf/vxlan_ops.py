import argparse
from utils.yaml_configs import YamlUtils

class VxlanConfig(YamlUtils):
    def __init__(self, vxlan_config_file):
        self.yaml_config=YamlUtils(vxlan_config_file)
        self.vxlan_config = self.yaml_config.parse_vxlan_config_yaml()

    def vxlan_config_prints(self):
        print(self.vxlan_config)

    def vxlan_config_get(self):
        return self.vxlan_config

    def vxlan_namespace_config_get(self):
        return self.vxlan_config.ns_config

    def vxlan_host_config_host(self):
        return self.vlxan_config.host_config


class VxlanOps:

parser = argparse.ArgumentParser(description='Vxlan Host Configuration')
parser.add_argument("--vxlanconfigfile", type=str, help="File to store generated conf")
args = parser.parse_args()

vxlan_config_ops=VxlanConfig(args.vxlanconfigfile)
vxlan_config_ops.vxlan_config_prints()

