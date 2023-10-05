# Procedure for bringing up hostapd and wpa_supplicant over 80211_hwsim

## Enable 80211-hwsim
* 80211-hwsim is enabled by default in the kernel but loaded as module
  ```
  grep HWSIM /boot/config-*
  /boot/config-5.4.0-155-generic:CONFIG_MAC80211_HWSIM=m
  ```
  
