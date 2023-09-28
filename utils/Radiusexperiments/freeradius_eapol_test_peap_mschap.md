# Radius Experiment with eapol_test and peap-mschapv2

## Topology
Main-Namespace (10.1.1.10) ----- (10.1.1.1) WifiSys-Namespace

## Configuration file

### For eopal_test
  Get the file : ./freeradius-server-3.2.3/src/tests/peap-mschapv2.conf

### For radius server
*peap-mode*
```
root@distro-magma:/usr/local/etc/raddb# cat  mods-available/eap | grep peap
        #  built, the "tls", "ttls", and "peap" sections will
                default_eap_type = peap
        peap {
```

*user*
```
root@distro-magma:/usr/local/etc/raddb# cat users  | grep yogesh
yogesh Cleartext-Password := "hellothere"
root@distro-magma:/usr/local/etc/raddb#
```

*clients.conf*
```
root@distro-magma:/usr/local/etc/raddb# cat clients.conf | grep WifiSys -A5
client WifiSys {
       secret          = my_Sup4r_SeCret_Pa$
       shortname       = Access-Point_Office
       ipaddr          = 10.1.1.1
}
```

## Test
*Main-Namespace*
``` root@distro-magma:/usr/local/etc/raddb# radiusd -X -f -x```

*WifiSys-Namespace*
```
root@distro-magma:/home/vagrant/EAPOL_TEST# ./eapol_test -c peap-mschapv2.conf -a10.1.1.10 -s my_Sup4r_SeCret_Pa$

root@distro-magma:/home/vagrant/EAPOL_TEST# ./eapol_test -c peap-mschapv2.conf -a10.1.1.10 -s my_Sup4r_SeCret_Pa$
Reading configuration file 'peap-mschapv2.conf'
Line: 1 - start of a new network block
ssid - hexdump_ascii(len=7):
     65 78 61 6d 70 6c 65                              example
key_mgmt: 0x1
eap methods - hexdump(len=16): 00 00 00 00 19 00 00 00 00 00 00 00 00 00 00 00
identity - hexdump_ascii(len=6):
     79 6f 67 65 73 68                                 yogesh
```
```
