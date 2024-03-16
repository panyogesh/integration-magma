# This section covers the PCF Configuration with Open5GS

## Topology
* Single Ubuntu VM: 20.0.4
* [Open5gs --- (127.0.0.X) ---- UERANSIM]

## Pre-Requisites
* Open5GS up and Running with default configuration
* UERANSSIM Up and Running with default configuration

## Brining up Open5GS
Reference: [Open5GS-using-Binary](https://open5gs.org/open5gs/docs/guide/01-quickstart/)
```
$ sudo apt update
$ sudo apt install wget gnupg
$ wget -qO - https://downloads.osmocom.org/packages/osmocom:/nightly/xUbuntu_20.04/Release.key | sudo apt-key add -
$ sudo sh -c "echo 'deb https://downloads.osmocom.org/packages/osmocom:/nightly/xUbuntu_20.04/ ./' > /etc/apt/sources.list.d/open5gs.list"
$ sudo apt update
$ sudo apt install open5gs
```

## Brining Up UERANSIM
References: [UERANSIM-Using-Source-Code](https://github.com/aligungr/UERANSIM/wiki/Installation)
```
git clone https://github.com/aligungr/UERANSIM
cd UERANSIM
sudo apt update
sudo apt upgrade
sudo apt install make
sudo apt install gcc
sudo apt install g++
sudo apt install libsctp-dev lksctp-tools
sudo apt install iproute2
sudo snap install cmake --classic
make
```

## Adding Subscriber in Open5gs
* Use the [script](https://raw.githubusercontent.com/panyogesh/integration-magma/main/info_open5gs/subscriber_script.sh)
* chmod 777 script.sh
* ./script.sh
  
## Launching of UERANSIM
* cd ~/UERANSIM/build
* [Terminal-1] : ./nr-gnb -c ../config/open5gs-gnb.yaml
* [Terminal-2]: sudo ./nr-ue -c ../config/open5gs-ue.yaml

## Running the PCF command
* First get the IP Address of UE either by
* Method:1 ifconfig
 ``` 
    - uesimtun0: flags=369<UP,POINTOPOINT,NOTRAILERS,RUNNING,PROMISC>  mtu 1400
        inet 10.45.0.8  netmask 255.255.255.255  destination 10.45.0.8
        inet6 fe80::f649:ccaa:22a3:45fe  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 12  bytes 688 (688.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
 * Method 2 : Command line
```
echo $(cat /var/log/open5gs/pcf.log | grep 'sm-policy-notify' | grep "ipv4Address" | awk 'END{print $5}')  | grep -o '"ipv4Address":"[^"]*' | awk -F'"' '{print $4}'
```

 * Execute the following command and substitute "REPLACE_STRING" with actual value
 * Curl command
```
curl  --http2-prior-knowledge -X 'POST'  '127.0.0.13:7777/npcf-policyauthorization/v1/app-sessions' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"ascReqData":{"afAppId":"IMS Services","dnn":"ims","evSubsc":{"events":[{"event":"CHARGING_CORRELATION"},{"event":"ANI_REPORT","notifMethod":"ONE_TIME"}]},"medComponents":{"0":{"codecs":["downlink\noffer\nm=audio 49000 RTP/AVP 116 99 97 105 100\r\nb=AS:41\r\nb=RS:512\r\nb=RR:1537\r\na=maxptime:240\r\na=des:qos mandatory local sendrecv\r\na=curr:qos local none\r\na=des:qos option","uplink\nanswer\nm=audio 50020 RTP/AVP 99 105\r\nb=AS:41\r\nb=RS:600\r\nb=RR:2000\r\na=rtpmap:99 AMR-WB/16000/1\r\na=fmtp:99 mode-change-capability=2;max-red=0\r\na=rtpmap:105 telephone-event/16"],"fStatus":"ENABLED","marBwDl":"96000 bps","marBwUl":"96000 bps","medCompN":0,"medSubComps":{"0":{"fNum":0,"fDescs":["permit out icmp from any to any","permit in icmp from any to any"],"flowUsage":"NO_INFO"},"1":{"fNum":1,"fDescs":["permit out 17 from 172.20.166.84 to 10.45.0.2 20002","permit in 17 from 10.45.0.18 to 172.20.166.84 20361"],"flowUsage":"RTCP"}},"medType":"AUDIO","rrBw":"2400 bps","rsBw":"2400 bps"}},"resPrio":"PRIO_1","notifUri":"http://127.0.0.16:7777/npcf-policyauthorization/v1/app-sessions/1","sponStatus":"SPONSOR_DISABLED","supi":"imsi-999700000000001","suppFeat":"12","ueIpv4":"REPLACE_STRING","ueIpv6":"::12"}}'
```
example
```
curl  --http2-prior-knowledge -X 'POST'  '127.0.0.13:7777/npcf-policyauthorization/v1/app-sessions' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"ascReqData":{"afAppId":"IMS Services","dnn":"ims","evSubsc":{"events":[{"event":"CHARGING_CORRELATION"},{"event":"ANI_REPORT","notifMethod":"ONE_TIME"}]},"medComponents":{"0":{"codecs":["downlink\noffer\nm=audio 49000 RTP/AVP 116 99 97 105 100\r\nb=AS:41\r\nb=RS:512\r\nb=RR:1537\r\na=maxptime:240\r\na=des:qos mandatory local sendrecv\r\na=curr:qos local none\r\na=des:qos option","uplink\nanswer\nm=audio 50020 RTP/AVP 99 105\r\nb=AS:41\r\nb=RS:600\r\nb=RR:2000\r\na=rtpmap:99 AMR-WB/16000/1\r\na=fmtp:99 mode-change-capability=2;max-red=0\r\na=rtpmap:105 telephone-event/16"],"fStatus":"ENABLED","marBwDl":"96000 bps","marBwUl":"96000 bps","medCompN":0,"medSubComps":{"0":{"fNum":0,"fDescs":["permit out icmp from any to any","permit in icmp from any to any"],"flowUsage":"NO_INFO"},"1":{"fNum":1,"fDescs":["permit out 17 from 172.20.166.84 to 10.45.0.2 20002","permit in 17 from 10.45.0.18 to 172.20.166.84 20361"],"flowUsage":"RTCP"}},"medType":"AUDIO","rrBw":"2400 bps","rsBw":"2400 bps"}},"resPrio":"PRIO_1","notifUri":"http://127.0.0.16:7777/npcf-policyauthorization/v1/app-sessions/1","sponStatus":"SPONSOR_DISABLED","supi":"imsi-999700000000001","suppFeat":"12","ueIpv4":"10.45.0.8","ueIpv6":"::12"}}'
```
