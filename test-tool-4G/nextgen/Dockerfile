# Docker command :-
# Build : 
#     sudo docker build -t enbsim:dec13 .
# Pre-burnt config :
#     sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 
# With Updated Configs
#     sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 "--mme_ip" "192.168.62.176" "--imsi" "724990000000009" "--mcc_mnc" "72499"
# sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13 "--mme_ip" "192.168.62.176" "--imsi" "724990000000009" "--mcc_mnc" "72499" "--connected_loop" True
# Python Simulator command :-
#     sudo python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000008 --mcc_mnc 72499
#     sudo python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000008 --mcc_mnc 72499 --enb_ip 192.168.62.154
#     sudo python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000008 --mcc_mnc 72499 --enb_ip 192.168.62.154 connected_loop=True
#
# Original fasferraz command
# Host Machine : sudo python3.8 /home/vagrant/eNB/eNB_LOCAL.py -i 192.168.62.154 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72499
# Docker Machine : python3.8 ./eNB_LOCAL.py -i 172.17.0.2 -m 192.168.62.176 -I 724990000000008 -K 465B5CE8B199B49FAA5F0A2EE238A6BC -C E8ED289DEBA952E4283B54E88E6183CA -o 72499

# Debugging the image
# Running in bash mode :-
# sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun --name appTest4G -it --entrypoint bash enbsim:dec13
# sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun --name appTest4G -it --network=enb_net --entrypoint bash enbsim:dec13

#                        sudo docker exec -it  gracious_heisenberg /bin/bash

# Patch generated using : git format-patch -1 HEAD

# Launch command : python3.8 launch_script.py --lower_limit  724990000000008 --upper_limit 724990000000018
# With Volumes : sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun -v /home/vagrant/integration-magma/test-tool-4G:/app/eNB/log --name appTest4G -it --entrypoint bash enbsim:dec13
 
FROM ubuntu:20.04

RUN apt update && apt install software-properties-common -y

RUN apt install python3.8

RUN apt-get install -y python3-pip libsctp-dev swig python3-pyscard git python3-netifaces python3-pexpect python3-paramiko iproute2 net-tools iputils-ping vim

WORKDIR /app

RUN git clone https://github.com/fasferraz/eNB.git /app/eNB

RUN ls

WORKDIR /app/eNB

RUN mkdir -p /app/eNB/log

ENV LOGPATH=/app/eNB/log

RUN git checkout 60f5196691bcfc25657b60b3a13bcb790adc7a2d

COPY 0001-feat-mutli-ue-per-gnb-support-Multi-UE-support.patch /app/eNB

RUN git apply 0001-feat-mutli-ue-per-gnb-support-Multi-UE-support.patch

RUN pip3 install -r requirements.txt

COPY SimLaunch.py  /app/eNB

ENV MME_IP_ADDRESS "192.168.62.176"

ENV IMSI_BASE "724990000000008"

ENV MCC_MNC_STR "72499"

ENV UPPER_LIMIT_IMSI "724990000000011"

ENV SERVICE_REQUEST True

ENV CONNECTED_LOOP False

CMD ["sh", "-c", "python3.8 /app/eNB/SimLaunch.py --mme_ip ${MME_IP_ADDRESS} --imsi  ${IMSI_BASE} --mcc_mnc ${MCC_MNC_STR} --upper_limit_imsi  ${UPPER_LIMIT_IMSI} --service_request ${SERVICE_REQUEST}"]

#CMD ["/bin/sh"]
