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
    - wget https://raw.github.com/panyogesh/integration-magma/blob/main/test-tool-4G/SimLaunch.py
* Change the parameters in Docker file based on the enviornment
    - MME_IP_ADDRESS="Remote IP of the Machine"
    - MCC_MNC_STR="MCCMNC" MCC+MNC to be used
    - in CMD options are [MME-IP, IMSI, MCCMNC]
* Key and OPC are already hardcoded in the SimLaunch.py
* BUILD COMMAND : sudo docker build -t enbsim:dec13 .
* RUN COMMAND : sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13
* OVERRIDE COMMAND : sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 "192.168.62.176" "724990000000008" "72499"
          