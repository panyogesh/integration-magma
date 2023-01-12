# Configuration details of IPSec on AGW

## Topology
(lo-1.1.1.1/32) AGW (eth1-192.168.62.176/24) ------------ (eth1-192.168.62.154/24) SIMULATOR (lo-2.2.2.2/32)


## Installation
sudo apt-get install strongswan


## AGW Configuration

### Pre-requisites

 - sudo sysctl -a | grep "ip_forward = 1"
 - sudo sysctl -a | grep "net.ipv4.conf.all.accept_redirects = 0"
 - sudo sysctl -a | grep "net.ipv4.conf.all.send_redirects = 0"

### Configuration

* Configure secondary IP-Address on loopback interface
  - sudo ip addr add 1.1.1.1/32 dev lo

    ```
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/0 scope host lo
           valid_lft forever preferred_lft forever
        inet 1.1.1.1/32 scope global lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    ```



* Configure PSK in ipsec.secrets
  - Contents of ipsec.secrets
    ```
    vagrant@distro-magma:~$ sudo cat /etc/ipsec.secrets
    # This file holds shared secrets or RSA private keys for authentication.

    # RSA private key for this host, authenticating it to any other host
    # which knows the public part.

    192.168.62.176 192.168.62.154 : PSK 'password123'
    vagrant@distro-magma:~$
    ```

* Configure charon listening interface as eth1
  - Charon configuration for specific interface
    ```
    vagrant@distro-magma:/$ sudo cat /etc/strongswan.d/charon.conf  | grep "interfaces_use ="
        interfaces_use = eth1
    vagrant@distro-magma:/$
    ```

* Configure ipsec.conf
  - ipsec.conf configuration

    ```
    vagrant@distro-magma:~$ cat /etc/ipsec.conf
    # ipsec.conf - strongSwan IPsec configuration file

    # basic configuration

config setup
        strictcrlpolicy=no
        uniqueids=yes
        charondebug = "all"

# Add connections here.
conn AGW_TO_SIMULATOR
        type=tunnel
        keyexchange=ikev2
        authby=secret
        left=192.168.62.176
        leftsubnet=1.1.1.1/32
        right=192.168.62.154
        rightsubnet=2.2.2.2/32
        ike=aes256-sha2_256-modp1024!
        esp=aes256-sha2_256!
        keyingtries=0
        ikelifetime=1h
        lifetime=8h
        dpddelay=30
        dpdtimeout=120
        dpdaction=restart
        auto=start
vagrant@distro-magma:~$
```


## SIMULATOR Configuration

### Pre-requisites
 - sudo sysctl -a | grep "ip_forward = 1"
 - sudo sysctl -a | grep "net.ipv4.conf.all.accept_redirects = 0"
 - sudo sysctl -a | grep "net.ipv4.conf.all.send_redirects = 0"

### Configuration

* Configure the secondary ip address on lo
  - sudo ip addr add 2.2.2.2/32 dev lo
    ```
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/0 scope host lo
           valid_lft forever preferred_lft forever
        inet 2.2.2.2/32 scope global lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    ```

* Configure PSK in ipsec.secrets
  - Configure the ipsec.secrets
    ```
    vagrant@oai-gnb-ue-sim:/var/log$ sudo cat /etc/ipsec.secrets
    # This file holds shared secrets or RSA private keys for authentication.

    # RSA private key for this host, authenticating it to any other host
    # which knows the public part.

    192.168.62.154 192.168.62.176 : PSK 'password123'
    vagrant@oai-gnb-ue-sim:/var/log$
    ```

* Configure charon listening interface as enp0s8
  - Configure the listening interface
    ``` 
    vagrant@oai-gnb-ue-sim:~$ sudo cat /etc/strongswan.d/charon.conf  | grep "interfaces_use ="
        interfaces_use = enp0s8
    vagrant@oai-gnb-ue-sim:~$
    ```

* Configure ipsec.secrets
  - Contents of ipsec.secrets
    ```
    vagrant@oai-gnb-ue-sim:/var/log$ sudo cat /etc/ipsec.secrets
    # This file holds shared secrets or RSA private keys for authentication.

    # RSA private key for this host, authenticating it to any other host
    # which knows the public part.

    192.168.62.154 192.168.62.176 : PSK 'password123'
    vagrant@oai-gnb-ue-sim:/var/log$ cat /etc/ipsec.conf
    # ipsec.conf - strongSwan IPsec configuration file
    ```

* Configuration of ipsec.conf
  - Contets of ipsec.conf

```
# basic configuration
config setup
        strictcrlpolicy=no
        uniqueids=yes
        charondebug="all"

# Add connections here.
conn SIMULATOR_TO_AGW
        type=tunnel
        keyexchange=ikev2
        authby=secret
        left=192.168.62.154
        leftsubnet=2.2.2.2/32
        right=192.168.62.176
        rightsubnet=1.1.1.1/32
        ike=aes256-sha2_256-modp1024!
        esp=aes256-sha2_256!
        keyingtries=0
        ikelifetime=1h
        lifetime=8h
        dpddelay=30
        dpdtimeout=120
        dpdaction=restart
        auto=start
vagrant@oai-gnb-ue-sim:/var/log$
```


## Validation

### AGW

* Check the ipsec status
  - Check output of "sudo ipsec statusall"

```
vagrant@distro-magma:~$ sudo ipsec statusall
Status of IKE charon daemon (strongSwan 5.8.2, Linux 5.4.0-136-generic, x86_64):
  uptime: 14 minutes, since Jan 11 08:09:35 2023
  malloc: sbrk 2703360, mmap 0, used 728752, free 1974608
  worker threads: 11 of 16 idle, 5/0/0/0 working, job queue: 0/0/0/0, scheduled: 3
  loaded plugins: charon aesni aes rc2 sha2 sha1 md5 mgf1 random nonce x509 revocation constraints pubkey pkcs1 pkcs7 pkcs8 pkcs12 pgp dnskey sshkey pem openssl fips-prf gmp agent xcbc hmac gcm drbg attr kernel-netlink resolve socket-default connmark stroke updown eap-mschapv2 xauth-generic counters
Listening IP addresses:
  192.168.62.176
Connections:
AGW_TO_SIMULATOR:  192.168.62.176...192.168.62.154  IKEv2, dpddelay=30s
AGW_TO_SIMULATOR:   local:  [192.168.62.176] uses pre-shared key authentication
AGW_TO_SIMULATOR:   remote: [192.168.62.154] uses pre-shared key authentication
AGW_TO_SIMULATOR:   child:  1.1.1.1/32 === 2.2.2.2/32 TUNNEL, dpdaction=restart
Security Associations (1 up, 0 connecting):
AGW_TO_SIMULATOR[2]: ESTABLISHED 14 minutes ago, 192.168.62.176[192.168.62.176]...192.168.62.154[192.168.62.154]
AGW_TO_SIMULATOR[2]: IKEv2 SPIs: 5f2ec0ac5a6a4d50_i 73b4e4b4705402a5_r*, pre-shared key reauthentication in 30 minutes
AGW_TO_SIMULATOR[2]: IKE proposal: AES_CBC_256/HMAC_SHA2_256_128/PRF_HMAC_SHA2_256/MODP_1024
AGW_TO_SIMULATOR{2}:  INSTALLED, TUNNEL, reqid 1, ESP SPIs: ce3f822c_i c25abe12_o
AGW_TO_SIMULATOR{2}:  AES_CBC_256/HMAC_SHA2_256_128, 0 bytes_i, 0 bytes_o, rekeying in 7 hours
AGW_TO_SIMULATOR{2}:   1.1.1.1/32 === 2.2.2.2/32
vagrant@distro-magma:~$
```


## SIMULATOR

* Check the ipsec status
  - Check output of "sudo ipsec statusall"

```
vagrant@oai-gnb-ue-sim:/var/log$ sudo ipsec statusall
Status of IKE charon daemon (strongSwan 5.8.2, Linux 5.4.0-136-generic, x86_64):
  uptime: 15 minutes, since Jan 11 08:09:39 2023
  malloc: sbrk 2703360, mmap 0, used 658624, free 2044736
  worker threads: 11 of 16 idle, 5/0/0/0 working, job queue: 0/0/0/0, scheduled: 4
  loaded plugins: charon aesni aes rc2 sha2 sha1 md5 mgf1 random nonce x509 revocation constraints pubkey pkcs1 pkcs7 pkcs8 pkcs12 pgp dnskey sshkey pem openssl fips-prf gmp agent xcbc hmac gcm drbg attr kernel-netlink resolve socket-default connmark stroke updown eap-mschapv2 xauth-generic counters
Listening IP addresses:
  192.168.62.154
Connections:
SIMULATOR_TO_AGW:  192.168.62.154...192.168.62.176  IKEv2, dpddelay=30s
SIMULATOR_TO_AGW:   local:  [192.168.62.154] uses pre-shared key authentication
SIMULATOR_TO_AGW:   remote: [192.168.62.176] uses pre-shared key authentication
SIMULATOR_TO_AGW:   child:  2.2.2.2/32 === 1.1.1.1/32 TUNNEL, dpdaction=restart
Security Associations (1 up, 0 connecting):
SIMULATOR_TO_AGW[1]: ESTABLISHED 15 minutes ago, 192.168.62.154[192.168.62.154]...192.168.62.176[192.168.62.176]
SIMULATOR_TO_AGW[1]: IKEv2 SPIs: 5f2ec0ac5a6a4d50_i* 73b4e4b4705402a5_r, pre-shared key reauthentication in 21 minutes
SIMULATOR_TO_AGW[1]: IKE proposal: AES_CBC_256/HMAC_SHA2_256_128/PRF_HMAC_SHA2_256/MODP_1024
SIMULATOR_TO_AGW{1}:  INSTALLED, TUNNEL, reqid 1, ESP SPIs: c25abe12_i ce3f822c_o
SIMULATOR_TO_AGW{1}:  AES_CBC_256/HMAC_SHA2_256_128, 0 bytes_i, 0 bytes_o, rekeying in 7 hours
SIMULATOR_TO_AGW{1}:   2.2.2.2/32 === 1.1.1.1/32
vagrant@oai-gnb-ue-sim:/var/log$
```


## PING VALIDATION
* Check the ping command

```
vagrant@distro-magma:~$ ping 2.2.2.2
PING 2.2.2.2 (2.2.2.2) 56(84) bytes of data.
64 bytes from 2.2.2.2: icmp_seq=1 ttl=64 time=0.857 ms


vagrant@oai-gnb-ue-sim:/var/log$ sudo tcpdump -i enp0s8 not port 22
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on enp0s8, link-type EN10MB (Ethernet), capture size 262144 bytes
08:25:21.119486 IP 192.168.62.176 > 192.168.62.154: ESP(spi=0xc25abe12,seq=0x7), length 136
^C^C08:25:21.119486 IP 1.1.1.1 > 2.2.2.2: ICMP echo request, id 950, seq 7, length 64
```
 
