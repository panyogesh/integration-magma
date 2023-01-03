# 4G TEST TOOL

## Overview
This tool is based on [fasferraz](https://github.com/fasferraz/eNB.git).
Its a wonderful tool for performing quick 4G testing including some level of scale test.
Have integrated this tool on docker so as to create a scenario based test.
Docker image uses the host interface for SCTP connection and uses a tun device
to mme UE-Interface

## Quick Start Steps
* Topology assumption
     <4G-Core> (192.168.62.176) ------ (192.168.62.154) Test-Tool
* Install dockers on the system
* Get the files : 
    - wget https://raw.githubusercontent.com/panyogesh/integration-magma/main/test-tool-4G/Dockerfile
    - wget https://raw.githubusercontent.com/panyogesh/integration-magma/main/test-tool-4G/SimLaunch.py
    - wget https://github.com/panyogesh/integration-magma/blob/main/test-tool-4G/0001-feat-integration-Integrated-with-client.patch
    - wget https://github.com/panyogesh/integration-magma/blob/main/test-tool-4G/0002-feat-tunname-Change-the-name-of-tunnel-per-config.patch
    
* Change the parameters in Docker file based on the enviornment
    - MME_IP_ADDRESS="Remote IP of the Machine"
    - MCC_MNC_STR="MCCMNC" MCC+MNC to be used
    - in CMD options are [MME-IP, IMSI, MCCMNC]
    
* Key and OPC are already hardcoded in the SimLaunch.py
* BUILD COMMAND : ```sudo docker build -t enbsim:dec13 .```

## For Host based networking
* RUN COMMAND : sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13
* OVERRIDE COMMAND : sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 "--mme_ip" "192.168.62.176" "--imsi" "724990000000009" "--mcc_mnc" "72499"

## For macvlan based networking
* docker network create -d macvlan --subnet=192.168.62.0/24 --gateway=192.168.62.1  -o parent=enp0s8 enb_net
* sudo ip link add mac0 link enp0s8 type macvlan mode bridge
* sudo ip addr add 192.168.62.71/24 dev mac0
* sudo ifconfig mac0 up
* sudo ip link set enp0s8 promisc on
* sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun -it --network=enb_net --entrypoint bash enbsim:dec13
* From Inside we can run the command : python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000008 --mcc_mnc 72499


          
