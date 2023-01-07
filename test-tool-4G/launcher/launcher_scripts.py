import subprocess
import time

mme_ip="192.168.62.176"
subs_range=range(724990000000008, 724990000000010)
mcc_mnc="72499"

for subs in subs_range:

    command_str=\
      "python3.8 SimLaunch.py --mme_ip {} --imsi {} --mcc_mnc {} --connected_loop True".format(\
      mme_ip, str(subs), mcc_mnc)

    subprocess.Popen(command_str.split())

    time.sleep (30)
