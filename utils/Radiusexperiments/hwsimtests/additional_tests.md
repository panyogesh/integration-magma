# Additional inbuilt hostapd tests to learn the behavior

## Pre-Requisites
* sudo apt-get install binutils-dev
* sudo apt-get install libsqlite3-dev
* sudo apt-get install libpcap-dev
* sudo pip install pycryptodome
* sudo pip install pyrad

## Steps to bring the repository
* git  clone git://w1.fi/hostap.git
* cd ~/hostap/hostapd
* cp ~/hostap/tests/hwsim/example-hostapd.config .config
* make clean
* make
* cd ~/hostap/wpa_supplicant/
* cp ~/hostap/tests/hwsim/example-wpa_supplicant.config .config
* make clean
* make hostapd hostapd_cli hlr_auc_gw

## Run thes tests
* cd ~/hostap/tests
* cd ~/hostap/tests/hwsim
* sudo ./start.sh
* sudo ./run-tests.py eap_proto
* sudo ./run-tests.py ap_wpa2_eap_aka






