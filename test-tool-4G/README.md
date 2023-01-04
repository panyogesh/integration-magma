# 4G TEST TOOL

## Overview
This tool is based on [fasferraz](https://github.com/fasferraz/eNB.git).
Its a wonderful tool for performing quick 4G testing.
Idea for putting up this repository is to integrate with our framework and create a flow based testing
where manually putting the values in tool is not required.

Also the idea was to have the solutions in docker so that it can mimick multi-enb scenarios as well

## Architecture
[ SimLaunch(client) -- Fassferraz(server) ] ----- 4GCore (MAMGA-AGW)

## Quick Start
* Please check the ```install``` directory   
    
* Change the parameters in Docker file based on the enviornment
    - MME_IP_ADDRESS="Remote IP of the Machine"
    - MCC_MNC_STR="MCCMNC" MCC+MNC to be used
    - in CMD options are [MME-IP, IMSI, MCCMNC]
    
## Current Support
* Host based networking (Using connected IP of host as eNB-IP)
* For macvlan based networking (Can have its own eNB-IP)

## Work under progress
* Traffic testing support
