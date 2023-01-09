import argparse
import os
import subprocess
import sys
import time

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--lower_limit', type=int,
                    help="Starting value of subscriber id", required=True)
PARSER.add_argument('--upper_limit', type=int,
                    help="Ending value of subscriber id", required=True)

ARGUMENTS = PARSER.parse_args()

if os.environ['MCC_MNC_STR']:
    mcc_mnc = os.environ['MCC_MNC_STR']
else:
    print(" MCC MNC not Found ")
    sys.exit()

if os.environ['MME_IP_ADDRESS']:
    mme_ip = os.environ['MME_IP_ADDRESS']
else:
    print(" MME IP is not found in env ")
    sys.exit()

subs_range=range(ARGUMENTS.lower_limit, ARGUMENTS.upper_limit)

for subs in subs_range:
    command_str=\
      "python3.8 SimLaunch.py --mme_ip {} --imsi {} --mcc_mnc {} --connected_loop True".format(\
      mme_ip, str(subs), mcc_mnc)

    subprocess.Popen(command_str.split())

    time.sleep (30)
