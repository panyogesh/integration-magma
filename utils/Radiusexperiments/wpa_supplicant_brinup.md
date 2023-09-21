# WPA Supplicant bring up

* wget https://w1.fi/releases/wpa_supplicant-2.10.tar.gz
* tar -zxvf wpa_supplicant-2.10.tar.gz
* cd wpa_supplicant-2.10/wpa_supplicant/
* cp defconfig .config  ``` CONFIG_EAP_AKA=y CONFIG_EAP_TLS=y```
* sudo apt install libssl-dev build-essential checkinstall  pkg-config
* sudo  apt install dbus libdbus-1-dev libdbus-glib-1-2 libdbus-glib-1-dev libreadline-dev libncurses5-dev
* sudo apt install libnl-genl-3-dev libnl-3-dev
* sudo apt install libnl-genl-3-dev libnl-route-3-dev
* CFLAGS=-Wno-deprecated-declarations make eapol_test




    
