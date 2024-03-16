echo " Creating the configuration file for Red "
python3.10 dictToYaml.py  --vxlanconfigfile=vxlanHostRed.yml --nscolor=red --nsip=192.168.60.13/16 --hostbridgeip=192.168.60.14/16 --vxlanid=100 --vxlanlocalip=192.168.60.11 --vxlanremoteip=192.168.60.12
echo " Creating the configuration file for Blue "
python3.10 dictToYaml.py  --vxlanconfigfile=vxlanHostBlue.yml --nscolor=blue --nsip=192.168.60.15/16 --hostbridgeip=192.168.60.16/16 --vxlanid=100 --vxlanlocalip=192.168.60.12 --vxlanremoteip=192.168.60.11
