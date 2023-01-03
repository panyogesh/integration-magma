# Docker command :-
# Build : 
#     sudo docker build -t enbsim:dec13 .
# Pre-burnt config :
#     sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 
# With Updated Configs
#     sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 "--mme_ip" "192.168.62.176" "--imsi" "724990000000009" "--mcc_mnc" "72499"

# Python Simulator command :-
#     sudo python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000008 --mcc_mnc 72499
#     sudo python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000008 --mcc_mnc 72499 --enb_ip 192.168.62.154
#
# Original fasferraz command
# Host Machine : sudo python3.8 /home/vagrant/eNB/eNB_LOCAL.py -i 192.168.62.154 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72499
# Docker Machine : python3.8 ./eNB_LOCAL.py -i 172.17.0.2 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72499

# Debugging the image
# Running in bash mode : sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun -it --entrypoint bash enbsim:dec13
#                        sudo docker exec -it  gracious_heisenberg /bin/bash

# Patch generated using : git format-patch -1 HEAD
 
FROM ubuntu:20.04

RUN apt update && apt install software-properties-common -y

RUN apt install python3.8

RUN apt-get install -y python3-pip libsctp-dev swig python3-pyscard git python3-netifaces python3-pexpect python3-paramiko iproute2

RUN apt-get install net-tools

RUN apt-get install iputils-ping

WORKDIR /app

RUN git clone https://github.com/fasferraz/eNB.git /app/eNB

RUN ls

WORKDIR /app/eNB

RUN git checkout 87f73ac0280e2d250df0d0bf71a914f42da0917a

COPY 0001-feat-integration-Integrated-with-client.patch /app/eNB

COPY 0002-feat-tunname-Change-the-name-of-tunnel-per-config.patch /app/eNB

RUN git apply 0001-feat-integration-Integrated-with-client.patch

RUN git apply 0002-feat-tunname-Change-the-name-of-tunnel-per-config.patch

RUN pip3 install -r requirements.txt

COPY SimLaunch.py  /app/eNB

ENV MME_IP_ADDRESS="192.168.62.176"

ENV MCC_MNC_STR=72499

ENTRYPOINT ["python3.8",  "/app/eNB/SimLaunch.py"]

CMD ["--mme_ip", "192.168.62.176", "--imsi", "724990000000008", "--mcc_mnc", "72499"]

#CMD ["/bin/sh"]
