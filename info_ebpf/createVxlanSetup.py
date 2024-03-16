import argparse
from pathlib import Path
import sys
import yaml


def create_namespace(args.nscolor) -> bool:


parser = argparse.ArgumentParser(description='Vxlan Host Configuration')
parser.add_argument("hostCfgFile")
args = parser.parse_args()

targetFile = Path(args.hostCfgFile)
if not targetFile:
    print("The target host configuration file does not exist")
    raise SystemExit(1)

#
# Sample contents
# {'color': 'red', 'ipaddrBridge': '192.168.60.14/16', 'ipaddrNs': '192.168.60.13/16', 
#  'outgoingIfName': 'veth1', 'vxlanLocalIP': '192.168.60.11', 'vxlanRemoteIP': '192.168.60.12',
#  'vxlanid': '100'}

with open(targetFile) as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
