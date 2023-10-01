# Experiments with hostapd and eapol_test

## Reference
https://github.com/enckse/hostapd-radius-eap-server/tree/master

## Pre-Requisites Steps
* https://github.com/enckse/hostapd-radius-eap-server.git
* make
* make install
* make certificates

## Configuration
* Server Side:
    cat bin/eap_users
    "user.name" PEAP
* Client Side:
     network={
        key_mgmt=WPA-EAP
        eap=PEAP
        identity="user.name"
        password="test"
        phase2="autheap=MSCHAPV2"
    }

## Test
* cd bin && ./hostapd hostapd.conf
* cd bin && ./eapol_test -a 127.0.0.1 -c eapol_test.conf -s secretclientkey -M 11:22:33:44:55:66


