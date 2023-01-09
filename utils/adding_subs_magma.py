#!/usr/bin/python3.8
import argparse
import subprocess
import time

def subsadd(lower_limit: int, upper_limit: int):
    subsadd="subscriber_cli.py  add --lte-auth-key 465B5CE8B199B49FAA5F0A2EE238A6BC --lte-auth-opc E8ED289DEBA952E4283B54E88E6183CA IMSI"
    subsupdate="subscriber_cli.py update --lte-auth-key 465B5CE8B199B49FAA5F0A2EE238A6BC --lte-auth-opc E8ED289DEBA952E4283B54E88E6183CA --apn-config internet,5,15,1,1,1000,2000,0,,,,  IMSI"

    subs_range=range(lower_limit, upper_limit)
    for subs in subs_range:
        cmd_add_str=subsadd + str(subs)
        cmd_update_str=subsupdate + str(subs)
        subprocess.Popen(cmd_add_str.split())
        time.sleep(0.500)
        subprocess.Popen(cmd_update_str.split())
        print(cmd_add_str)
        print(cmd_update_str)
        print("   ")
        time.sleep(0.500)

def subsdel(lower_limit: int, upper_limit: int):
    subs_range=range(lower_limit, upper_limit)
    for subs in subs_range:
        cmd_del_str="subscriber_cli.py delete IMSI{}".format(subs)
        subprocess.Popen(cmd_del_str.split())
        print(cmd_del_str)
        time.sleep(0.500)

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--add_loop', type=bool, default=False)

ARGUMENTS = PARSER.parse_args()

lower_limit=724990000000008
upper_limit=724990000000308

if ARGUMENTS.add_loop:
    subsadd(lower_limit, upper_limit)
else:
    subsdel(lower_limit, upper_limit)
