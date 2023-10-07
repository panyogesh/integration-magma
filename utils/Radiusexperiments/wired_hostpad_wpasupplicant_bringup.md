# Tutorial for hostapd & wpa_supplicant connection for wired connection

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
    
