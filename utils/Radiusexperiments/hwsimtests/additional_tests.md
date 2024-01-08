# Additional inbuilt hostapd tests to learn the behavior

## Pre-Requisites
* sudo apt-get install binutils-dev
* sudo apt-get install libsqlite3-dev
* sudo apt-get install libpcap-dev
* sudo apt-get install python3-pip
* sudo pip install pycryptodome
* sudo pip install pyrad
* sudo apt install libssl-dev build-essential checkinstall  pkg-config
* sudo  apt install dbus libdbus-1-dev libdbus-glib-1-2 libdbus-glib-1-dev libreadline-dev libncurses5-dev
* sudo apt install libnl-genl-3-dev libnl-3-dev
* sudo apt install libnl-genl-3-dev libnl-route-3-dev
* sudo apt install libiberty-dev zlib1g-dev

## Steps to bring the repository
* git  clone git://w1.fi/hostap.git
* cd ~/hostap/hostapd
* cp ../tests/hwsim/example-hostapd.config .config
* make clean
* make
* cd ../wpa_supplicant/
* cp ../hostap/tests/hwsim/example-wpa_supplicant.config .config
* make clean
* make hostapd hostapd_cli hlr_auc_gw

## Run thes tests
* cd ~/hostap/tests
* cd ~/hostap/tests/hwsim
* sudo ./start.sh
* sudo ./run-tests.py eap_proto
* sudo ./run-tests.py ap_wpa2_eap_aka

## Additional Reference
https://github.com/clearlinux/distribution/issues/640




