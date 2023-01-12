# Configuration 5G Call flow on AGW

## Topology
(lo-1.1.1.1/32) AGW (eth1-192.168.62.176/24) ------------ (eth1-192.168.62.154/24) SIMULATOR (lo-2.2.2.2/32)

## Configuration & Changes in magma

### Minor changes
* Only temporary. Will be removed going forward

```
vagrant@distro-magma:/etc/magma$ diff -r -u /usr/local/lib/python3.8/dist-packages/magma/common/misc_utils.py.orig /usr/local/lib/python3.8/dist-packages/magma/common/misc_utils.py
--- /usr/local/lib/python3.8/dist-packages/magma/common/misc_utils.py.orig      2023-01-11 09:57:36.790136786 +0000
+++ /usr/local/lib/python3.8/dist-packages/magma/common/misc_utils.py   2023-01-11 10:29:32.894156747 +0000
@@ -37,12 +37,16 @@
     """
     # Raises ValueError if interface is unavailable
     ip_addresses = netifaces.ifaddresses(interface)
-
+
+    index=0
+    if ip_addresses[netifaces.AF_INET][0]['addr'] == '127.0.0.1':
+        if len(ip_addresses[netifaces.AF_INET]) == 2:
+            index=1

     try:
         ipv4_address = (
-            ip_addresses[netifaces.AF_INET][0]['addr'],
-            ip_addresses[netifaces.AF_INET][0]['netmask'],
+            ip_addresses[netifaces.AF_INET][index]['addr'],
+            ip_addresses[netifaces.AF_INET][index]['netmask'],
         )
     except KeyError:
         ipv4_address = None
vagrant@distro-magma:/etc/magma$
```

### Renaming outgoing SCTP port

* Replace eth1 with lo in "/etc/magma"
``` sudo sed -i 's/eth1/lo/g' *```

* Enable 5G configuration
``` sudo sed -i 's/\"enable5gFeatures\": false/\"enable5gFeatures\": true/g' gateway.mconfig ```


## Configuration & Changes in SIMULATOR

MME/AMF-IP : 1.1.1.1/32
GNB IP : 2.2.2.2/32
GTP IP : 2.2.2.2/32

## VALIDATION LOGS

```
vagrant@distro-magma:/etc/magma$ sudo ovs-ofctl dump-flows gtp_br0 table=0 | grep tun
 cookie=0x0, duration=2.711s, table=0, n_packets=0, n_bytes=0, idle_age=2, priority=65503,tun_id=0x7fffffff,qfi=5,in_port=32768 actions=mod_dl_src:02:00:00:00:00:01,mod_dl_dst:ff:ff:ff:ff:ff:ff,set_field:0xc9accc06->reg9,load:0x149aff1b536041->OXM_OF_METADATA[],resubmit(,1)
vagrant@distro-magma:/etc/magma$
```

```
vagrant@distro-magma:~$ sudo ipsec statusall
Status of IKE charon daemon (strongSwan 5.8.2, Linux 5.4.0-136-generic, x86_64):
  uptime: 95 minutes, since Jan 11 13:28:22 2023
  malloc: sbrk 2703360, mmap 0, used 908656, free 1794704
  worker threads: 11 of 16 idle, 5/0/0/0 working, job queue: 0/0/0/0, scheduled: 4
  loaded plugins: charon aesni aes rc2 sha2 sha1 md5 mgf1 random nonce x509 revocation constraints pubkey pkcs1 pkcs7 pkcs8 pkcs12 pgp dnskey sshkey pem openssl fips-prf gmp agent xcbc hmac gcm drbg attr kernel-netlink resolve socket-default connmark stroke updown eap-mschapv2 xauth-generic counters
Listening IP addresses:
  192.168.62.176
Connections:
AGW_TO_SIMULATOR:  192.168.62.176...192.168.62.154  IKEv2, dpddelay=30s
AGW_TO_SIMULATOR:   local:  [192.168.62.176] uses pre-shared key authentication
AGW_TO_SIMULATOR:   remote: [192.168.62.154] uses pre-shared key authentication
AGW_TO_SIMULATOR:   child:  1.1.1.1/32 === 2.2.2.2/32 TUNNEL, dpdaction=restart
Security Associations (1 up, 0 connecting):
AGW_TO_SIMULATOR[4]: ESTABLISHED 19 minutes ago, 192.168.62.176[192.168.62.176]...192.168.62.154[192.168.62.154]
AGW_TO_SIMULATOR[4]: IKEv2 SPIs: 4d3c62333d6917ea_i* 5c8a5aa18affcef1_r, pre-shared key reauthentication in 21 minutes
AGW_TO_SIMULATOR[4]: IKE proposal: AES_CBC_256/HMAC_SHA2_256_128/PRF_HMAC_SHA2_256/MODP_1024
AGW_TO_SIMULATOR{4}:  INSTALLED, TUNNEL, reqid 3, ESP SPIs: c9f2726f_i c982fdec_o
AGW_TO_SIMULATOR{4}:  AES_CBC_256/HMAC_SHA2_256_128, 0 bytes_i, 0 bytes_o, rekeying in 7 hours
AGW_TO_SIMULATOR{4}:   1.1.1.1/32 === 2.2.2.2/32
vagrant@distro-magma:~$
```
