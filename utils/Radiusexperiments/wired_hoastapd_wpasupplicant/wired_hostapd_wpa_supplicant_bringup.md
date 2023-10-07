# Setup for hostapd & wpa_supplicant connection for wired connection
## Machine
ubuntu:20.04

## Topology
wiredns0 (veth0) ----- (veth1) wiredns1

## Configuration
```
sudo ip netns add wiredns0
sudo ip netns add wiredns1
sudo ip link add veth0 type veth peer name veth1

sudo ip link set veth0 netns wiredns0
sudo ip link set veth1 netns wiredns1
sudo ip netns exec wiredns0 ip addr add 30.0.0.1/24 dev veth0
sudo ip netns exec wiredns1 ip addr add 30.0.0.2/24 dev veth1
sudo ip netns exec wiredns0 ifconfig veth0 up
sudo ip netns exec wiredns1 ifconfig veth1 up
```

## Generating Certificates
* openssl genrsa -out server.key 2048
* openssl req -new -sha256 -key server.key -out csr.csr
  ```
  Country Name (2 letter code) [AU]:US
  State or Province Name (full name) [Some-State]:California
  Locality Name (eg, city) []:Melono Park
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:mycompany
  Organizational Unit Name (eg, section) []:Connectivity
  Common Name (e.g. server FQDN or YOUR name) []:Yogesh
  Email Address []:yogesh@mycompany.ai

  Please enter the following 'extra' attributes
  to be sent with your certificate request
  A challenge password []:
  An optional company name []:
  ```
* openssl req -x509 -sha256 -days 365 -key server.key -in csr.csr -out server.pem
* openssl dhparam 2048 > dhparam.pem
* ln -s server.pem ca.pem

## Launching hostapd
* sudo ../hostapd [wired_hostapd.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/conf_files/wired_hostapd/wired_hostapd.conf) -dd
```
EAP-PEAP: SUCCESS_REQ -> SUCCESS
EAP-PEAP: Derived key - hexdump(len=64): 56 c7 27 ab ce 82 10 96 67 98 7c c4 4c 3e 15 e7 ea aa df f3 d8 d5 5e 6e 16 49 02 e1 f5 44 bb b0 62 c5 1e 68 6d d9 95 36 2f 26 86 f6 9d cd 8c 02 04 7a fc b5 18 1f 23 35 7c 33 24 85 d0 85 e3 28
EAP: Session-Id - hexdump(len=65): 19 54 13 89 32 b0 b6 7c a8 29 7f 60 ae 36 1d 69 02 4d 69 ae e5 70 63 86 ed df bf 89 d2 d1 2b a1 85 6e 22 d9 ea 0c 96 45 47 d9 77 1b 7e 7c 57 0e b1 cb 44 9c 11 45 c4 dd 4d d2 cc 81 47 fb 60 a3 3a
EAP: EAP entering state SELECT_ACTION
EAP: getDecision: method succeeded -> SUCCESS
EAP: EAP entering state SUCCESS
EAP: Building EAP-Success (id=137)
veth0: CTRL-EVENT-EAP-SUCCESS 6a:04:fd:3e:7c:91
IEEE 802.1X: 6a:04:fd:3e:7c:91 BE_AUTH entering state SUCCESS
veth0: STA 6a:04:fd:3e:7c:91 IEEE 802.1X: Sending EAP Packet (identifier 137)
IEEE 802.1X: 6a:04:fd:3e:7c:91 AUTH_PAE entering state AUTHENTICATED
veth0: AP-STA-CONNECTED 6a:04:fd:3e:7c:91
veth0: STA 6a:04:fd:3e:7c:91 IEEE 802.1X: authorizing port
veth0: STA 6a:04:fd:3e:7c:91 RADIUS: starting accounting session 7A057DD4CBE7EB89
veth0: STA 6a:04:fd:3e:7c:91 IEEE 802.1X: authenticated - EAP type: 0 (unknown)
IEEE 802.1X: 6a:04:fd:3e:7c:91 BE_AUTH entering state IDLE
IEEE 802.1X: 6a:04:fd:3e:7c:91 - (EAP) retransWhile --> 0
IEEE 802.1X: 6a:04:fd:3e:7c:91 - aWhile --> 0
```

*  ../wpa_supplicant -i veth1 -c ./[wired_wpa_supplicant.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/conf_files/wired_wpa_supplicant/wired_wpa_supplicant.conf)  -Dwired -dd -K
```
EAP: EAP entering state IDLE
EAPOL: SUPP_BE entering state RESPONSE
EAPOL: txSuppRsp
TX EAPOL: dst=01:80:c2:00:00:03
TX EAPOL - hexdump(len=10): 01 00 00 06 02 89 00 06 19 01
EAPOL: SUPP_BE entering state RECEIVE
l2_packet_receive: src=d6:b6:a3:82:8c:52 len=8
veth1: RX EAPOL from d6:b6:a3:82:8c:52
RX EAPOL - hexdump(len=8): 02 00 00 04 03 89 00 04
EAPOL: Received EAP-Packet frame
EAPOL: SUPP_BE entering state REQUEST
EAPOL: getSuppRsp
EAP: EAP entering state RECEIVED
EAP: Received EAP-Success
EAP: Status notification: completion (param=success)
EAP: EAP entering state SUCCESS
veth1: CTRL-EVENT-EAP-SUCCESS EAP authentication completed successfully
EAPOL: IEEE 802.1X for plaintext connection; no EAPOL-Key frames required
veth1: WPA: EAPOL processing complete
veth1: Cancelling authentication timeout
veth1: State: ASSOCIATED -> COMPLETED
veth1: CTRL-EVENT-CONNECTED - Connection to 01:80:c2:00:00:03 completed [id=0 id_str=]
EAPOL: SUPP_PAE entering state AUTHENTICATED
EAPOL: Supplicant port status: Authorized
EAPOL: SUPP_BE entering state RECEIVE
EAPOL: SUPP_BE entering state SUCCESS
EAPOL: SUPP_BE entering state IDLE
EAPOL authentication completed - result=SUCCESS
EAPOL: authWhile --> 0
```
