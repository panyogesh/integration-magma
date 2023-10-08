# Configuration procedure eap-sim using hostapd and wpa_supplicant

## Configuration
Same as that of [link](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/wired_hostapd_wpa_supplicant_bringup.md)

## Generating Certificates
Same as that of [link](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/wired_hostapd_wpa_supplicant_bringup.md)

## Launching hostapd
* sudo ./hlr_auc_gw -u -m ../[hlr_auc_gw.milenage_db](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/eapaka_conf/hlr_auc_gw.milenage_db)
* sudo ../hostapd [eap_aka_hostapd.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/eapaka_conf/eap_sim_hostapd.conf) -dd
* ../wpa_supplicant -i veth1 -c ./[eap_aka_wpa_supplicant.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/eapaka_conf/eap_aka_wpa_supplicant.conf) -Dwired -dd -K

## Test Logs
![image](https://github.com/panyogesh/integration-magma/assets/69527565/8c141e87-8495-41f9-bae9-3e252b446ab9)


## Reference
https://stackoverflow.com/questions/41639359/test-eap-sim-with-hostapd-and-wpa-supplicant
