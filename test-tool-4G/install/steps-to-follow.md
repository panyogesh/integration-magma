# Installation instruction for running 4G test tool

## Connections & Topology
* Mac-4G-TestTool (enp0s8, 192.168.62.154) ----- (eth1, 192.168.62.176) MAGMA
* MCC/MNC : 724/99

## Machine preparation
* sudo apt install net-tools
* sudo apt  install docker.io

## Checking out the code
* git clone --depth 1 --no-checkout https://github.com/panyogesh/integration-magma.git
* cd integration-magma
* git sparse-checkout set test-tool-4G
* cd test-tool-4G/

## Preparing the docker build
* sudo docker build -t enbsim:dec13 .

## Host machine based execution
* sudo docker run  --name enbsim-app --cap-add=NET_ADMIN --device /dev/net/tun --rm  enbsim:dec13

## Macvlan based execution
* sudo docker network create -d macvlan --subnet=192.168.62.0/24 --gateway=192.168.62.1 -o parent=enp0s8 enb_net
* sudo ip link add mac0 link enp0s8 type macvlan mode bridge
* sudo ip addr add 192.168.62.72/24 dev mac0
* sudo ifconfig mac0 up
* sudo ip link set enp0s8 promisc on
* sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun -it --network=enb_net --entrypoint bash enbsim:dec13
* python3.8 SimLaunch.py --mme_ip 192.168.62.176 --imsi 724990000000009 --mcc_mnc 72499 --connected_loop True

