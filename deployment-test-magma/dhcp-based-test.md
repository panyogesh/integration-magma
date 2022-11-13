# DHCP based testing
Changes
 - Configuration for allocating ip address to subscriber using DHCP server
 - Reference PR : [#3291](https://github.com/magma/magma/pull/3291)

Test Case
 - UERANSIM & Magma AGW 2 Subsciber and PDU Creation



## TOPOLOGY

```bash
UERANSIM (enp0s8, enp0s9) ======= (eth1, eth2) AGW
--> inet 192.168.88.154/24 brd 192.168.88.255 scope global enp0s8
--> inet 192.168.89.64/24 brd 192.168.89.255 scope global enp0s9

<-- inet 192.168.88.176/24 brd 192.168.88.255 scope global eth1
< -- eth2 No Ip address:
< -- inet 192.168.129.1/24 scope global uplink_br0
```

## CONFIGURATIONS

### UERANSIM

* Installing the DHCP Server
 ```sudo apt install isc-dhcp-server```


* Modify the dhcp configuration

```bash
cat /etc/dhcp/dhcpd.conf

option domain-name-servers 8.8.8.8;
authoritative;

default-lease-time 600;
max-lease-time 7200;
always-broadcast on;
ddns-update-style none;

subnet 192.168.89.0 netmask 255.255.255.0 {
  range 192.168.89.2 192.168.89.63;
}
```

* Change the dhcp-server setting to point to enp0s9
```bash
vagrant@oai-gnb-ue-sim:~$ cat /etc/default/isc-dhcp-server
INTERFACESv4="enp0s9"
INTERFACESv6=""
vagrant@oai-gnb-ue-sim:~$
```

* Restart the dhcp services
```bash
  sudo systemctl restart isc-dhcp-server.service
  sudo systemctl status isc-dhcp-server.service

vagrant@oai-gnb-ue-sim:~$ sudo systemctl status isc-dhcp-server.service
? isc-dhcp-server.service - ISC DHCP IPv4 server
     Loaded: loaded (/lib/systemd/system/isc-dhcp-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-11-08 17:28:18 UTC; 2s ago
       Docs: man:dhcpd(8)
   Main PID: 71834 (dhcpd)
      Tasks: 4 (limit: 7089)
     Memory: 4.9M
     CGroup: /system.slice/isc-dhcp-server.service
             +-71834 dhcpd -user dhcpd -group dhcpd -f -4 -pf /run/dhcp-server/dhcpd.pid -cf /etc/dhcp/dhcpd.co>
```

## AGW

Configuration on agw

```bash
gagan@saturn:~/MAGMA_DIR/magma$ git diff lte/gateway/configs/gateway.mconfig lte/gateway/configs/pipelined.yml
diff --git a/lte/gateway/configs/gateway.mconfig b/lte/gateway/configs/gateway.mconfig
index 36aaab768e..368824fad2 100644
--- a/lte/gateway/configs/gateway.mconfig
+++ b/lte/gateway/configs/gateway.mconfig
@@ -69,7 +69,7 @@
       "csfbMnc": "01",
       "dnsPrimary": "8.8.8.8",
       "dnsSecondary": "8.8.4.4",
-      "enable5gFeatures": false,
+      "enable5gFeatures": true,
       "enableDnsCaching": false,
       "hssRelayEnabled": false,
       "ipv4PCscfAddress": "172.27.23.150",
@@ -90,12 +90,12 @@
     "mobilityd": {
       "@type": "type.googleapis.com/magma.mconfig.MobilityD",
       "ipBlock": "192.168.128.0/24",
-      "ip_allocator_type": "IP_POOL",
+      "ip_allocator_type": "DHCP",
       "ipv6Block": "fdee:5:6c::/48",
       "ipv6PrefixAllocationType": "RANDOM",
       "logLevel": "INFO",
       "multi_apn_ip_alloc": true,
-      "static_ip_enabled": true
+      "static_ip_enabled": false
     },
     "monitord": {
       "@type": "type.googleapis.com/magma.mconfig.MonitorD",
@@ -106,7 +106,7 @@
       "@type": "type.googleapis.com/magma.mconfig.PipelineD",
       "allowedGrePeers": [],
       "apps": [],
-      "enable5gFeatures": false,
+      "enable5gFeatures": true,
       "liUes": {},
       "logLevel": "INFO",
       "natEnabled": true,
@@ -127,7 +127,7 @@
     },
     "sessiond": {
       "@type": "type.googleapis.com/magma.mconfig.SessionD",
-      "enable5gFeatures": false,
+      "enable5gFeatures": true,
       "gxGyRelayEnabled": false,
       "logLevel": "INFO",
       "relayEnabled": false
@@ -150,7 +150,7 @@
     },
     "subscriberdb": {
       "@type": "type.googleapis.com/magma.mconfig.SubscriberDB",
-      "enable5gFeatures": false,
+      "enable5gFeatures": true,
       "logLevel": "INFO",
       "lteAuthAmf": "gAA=",
       "lteAuthOp": "EREREREREREREREREREREQ==",
@@ -164,4 +164,4 @@
       "throttleWindow": 5
     }
   }
-}
\ No newline at end of file
+}
diff --git a/lte/gateway/configs/pipelined.yml b/lte/gateway/configs/pipelined.yml
index 05f09f9c40..7e0f4f537e 100644
--- a/lte/gateway/configs/pipelined.yml
+++ b/lte/gateway/configs/pipelined.yml
@@ -165,9 +165,9 @@ ovs_internal_sampling_port_number: 15578
 # # Table to forward packets from the internal sampling port
 ovs_internal_sampling_fwd_tbl_number: 201
 # Be careful changing these default values
-# enable_nat: True
+enable_nat: False
 non_nat_gw_probe_frequency: 20
-# non_nat_arp_egress_port: dhcp0
+non_nat_arp_egress_port: dhcp0
 ovs_uplink_port_name: patch-up
 # virtual_mac: '02:ff:bb:cc:dd:ee'
 uplink_bridge: uplink_br0
gagan@saturn:~/MAGMA_DIR/magma$
```

