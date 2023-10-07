# Configuration procedure eap-sim using hostapd and wpa_supplicant

## Configuration
Same as that of [link](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/wired_hostapd_wpa_supplicant_bringup.md)

## Generating Certificates
Same as that of [link](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/wired_hostapd_wpa_supplicant_bringup.md)

## Launching hostapd
* sudo ./hlr_auc_gw -u -m ../hlr_auc_gw.milenage_db
* sudo ../hostapd [eap_sim_hostapd.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/eapsim_conf/eap_sim_hostapd.conf) -dd
* ../wpa_supplicant -i veth1 -c ./[eap_sim_wpa_supplicant.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wired_hoastapd_wpasupplicant/eapsim_conf/eap_sim_wpa_supplicant.conf)

## Test Logs
![image](https://github.com/panyogesh/integration-magma/assets/69527565/65b824e9-7206-45ad-a8a0-95f50f48d8e4)
