# EAP-TLS how to notes using free radius and eapol_test

## Fetch the freeradius code
- git clone https://github.com/FreeRADIUS/freeradius-server.git
- cd freeradius-server/
- git remote update
- git checkout v3.2.3
- git checkout origin/v3.2.x
- sudo apt-get install libtalloc-devel
- sudo apt-get install libtalloc-dev

## Apply the changes
- wget [eap-tls-experiment-freeradius.diff](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/Radiusexperiments/freeradius/eap-tls-bringup/eap-tls-experiment-freeradius.diff)
- patch -p1 < eap-tls-experiment-freeradius.diff

## Compile the code for radius server
- ./configure --with-modules="rlm_sim" --with-modules="rlm_sim_files"  --prefix
- make
- sudo make install

## Compile the code for eapol_test
- cd freeradius-server/scripts/ci/
- ./eapol_test-build.sh

## Configuration

### Radius server
  - raddb/certs/ca.cnf b/raddb/certs/ca.cnf
  - raddb/certs/client.cnf b/raddb/certs/client.cnf
  - raddb/certs/server.cnf b/raddb/certs/server.cnf
  - raddb/mods-available/eap b/raddb/mods-available/eap
  - raddb/sites-available/default b/raddb/sites-available/default

### eapol_test configuration

```
vagrant@distro-magma:~/freeradius-server/scripts/ci/eapol_test$ cat wpa_supplicant-TLS.conf
ap_scan=0

network={
    eap=TLS
    eapol_flags=0
    key_mgmt=IEEE8021X

    identity="client@mycompany.org"    
    client_cert="/home/vagrant/freeradius-server/raddb/certs/client.pem"
    private_key="/home/vagrant/freeradius-server/raddb/certs/client.key"
    private_key_passwd="clientmypassword"

    # CA certificate to validate the RADIUS server's identity
    ca_cert="/home/vagrant/freeradius-server/raddb/certs/ca.pem"
}
```

## Testing
* Terminal 1:
sudo radiusd -d ./raddb -X

* Terminal 2:
./eapol_test -c ./wpa_supplicant-TLS.conf -a 127.0.0.1 -s testing123
  

## Output
Terminal 1: radiusd
```
(6) Sent Access-Accept Id 6 from 127.0.0.1:1812 to 127.0.0.1:54687 length 188
(6)   MS-MPPE-Recv-Key = 0xedcc887c8153708f4a1832facef38084f80bacf9bee8e1a2510ceb2ca0400baf
(6)   MS-MPPE-Send-Key = 0x70f82576f42244ae9b55fa55c8303eb3ecf8f4be145d640d3e429b5e46876b3b
(6)   EAP-Message = 0x03c80004
(6)   Message-Authenticator = 0x00000000000000000000000000000000
(6)   User-Name = "client@mycompany.org"
(6)   Framed-MTU += 994
(6) Finished request
```

Terminal 2: eapol_test
```
EAPOL: SUPP_PAE entering state AUTHENTICATED
EAPOL: SUPP_BE entering state RECEIVE
EAPOL: SUPP_BE entering state SUCCESS
EAPOL: SUPP_BE entering state IDLE
eapol_sm_cb: result=1
EAPOL: Successfully fetched key (len=32)
PMK from EAPOL - hexdump(len=32): ed cc 88 7c 81 53 70 8f 4a 18 32 fa ce f3 80 84 f8 0b ac f9 be e8 e1 a2 51 0c eb 2c a0 40 0b af
No EAP-Key-Name received from server
WPA: Clear old PMK and PTK
EAP: deinitialize previously used EAP method (13, TLS) at EAP deinit
ENGINE: engine deinit
MPPE keys OK: 1  mismatch: 0
SUCCESS
```

## Issues
Freeradius 3.0.15 failing to read server.pem file 
    - https://lists.freeradius.org/pipermail/freeradius-users/2019-May/095470.html

## Reference
* https://wiki.freeradius.org/guide/eduroam
* https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/assembly_setting-up-an-802-1x-network-authentication-service-for-lan-clients-using-hostapd-with-freeradius-backend_configuring-and-managing-networking#proc_testing-eap-tls-authentication-against-a-freeradius-server-or-authenticator_assembly_setting-up-an-802-1x-network-authentication-service-for-lan-clients-using-hostapd-with-freeradius-backend
