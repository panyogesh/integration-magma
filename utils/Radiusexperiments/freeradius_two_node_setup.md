# Setting up free radius across two machines

## Installation
Refer to link for [my-freeradius](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/freeradius_bringup_basic_test.md)  installation.

## Topology
 ``` main-namespace (veth0) -------(veth1) WifiSys-namespace```

## Commands for setting up namespace
* sudp ip netns add WifiSys
* sudo ip link add veth0 type veth peer name veth1
* sudo ip link set veth1 netns WifiSys
* sudo ip netns exec WifiSys ip addr add 10.1.1.1/24 dev veth1
* sudo ip netns exec WifiSys ip link set dev veth1 up
* sudo ip addr add 10.1.1.10/24 dev veth0
* sudo ip link set dev veth0 up

## Configuration for setting up 
- /usr/local/etc/raddb
- file: users -> testuser1    Cleartext-Password := "mysecretpassword"
  
![image](https://github.com/panyogesh/integration-magma/assets/69527565/c841c16e-6496-4f40-8a34-1a48430eea7f)

- file: clients.conf -> client WifiSys
  
  ![image](https://github.com/panyogesh/integration-magma/assets/69527565/2657c8fc-045f-46b5-8046-2dd9d70cde31)

  ## Test setup
  - main-namespace
     cmd:
     ```radiusd -X```
  - WifiSys-namespace
     cmd:
      ```radtest testuser1 "mysecretpassword" 10.1.1.10 1812 my_Sup4r_SeCret_Pa$```

  Output
  ```
  root@distro-magma:/home/vagrant# radtest testuser1 "mysecretpassword" 10.1.1.10 1812 my_Sup4r_SeCret_Pa$
  Sent Access-Request Id 18 from 0.0.0.0:8016 to 10.1.1.10:1812 length 79
        User-Name = "testuser1"
        User-Password = "mysecretpassword"
        NAS-IP-Address = 127.0.2.1
        NAS-Port = 1812
        Message-Authenticator = 0x00
        Cleartext-Password = "mysecretpassword"
   Received Access-Accept Id 18 from 10.1.1.10:714 to 10.1.1.1:32790 length 20
   ```

  
