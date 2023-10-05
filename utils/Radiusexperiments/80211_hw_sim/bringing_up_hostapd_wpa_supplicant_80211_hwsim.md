# Procedure for bringing up hostapd and wpa_supplicant over 80211_hwsim

## Building hostapd and wpa_supplicant
* [hostapd-compilation](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/hostpad_bringup.md)
* [wpa_supplicant-compilation](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/wpa_supplicant_bringup.md)

## Enable 80211-hwsim
* 80211-hwsim is enabled by default in the kernel but loaded as module
  ```
  grep HWSIM /boot/config-*
  /boot/config-5.4.0-155-generic:CONFIG_MAC80211_HWSIM=m
  ```
* sudo apt install linux-generic
* sudo modprobe mac80211_hwsim
```
     vagrant@exp-2004-ubuntu:/lib/modules/5.4.0-163-generic$ lsmod | grep mac
     mac80211_hwsim         61440  0
     mac80211              847872  1 mac80211_hwsim
     cfg80211              708608  2 mac80211_hwsim,mac80211
     libarc4                16384  1 mac80211
    vagrant@exp-2004-ubuntu:/lib/modules/5.4.0-163-generic$
```

  ## Topology
  ```namespace-ns0 phy0 --------- phy1 namespace-ns1```
  
  ## Creating Namespace and attaching the links

  ```
  sudo ip netns add ns0
  sudo ip netns add ns1
  sudo iw phy phy0 set netns name ns0
  sudo iw phy phy1 set netns name ns1
  sudo ip netns exec ns0 ip addr add 20.0.0.1/24 dev wlan0
  sudo ip netns exec ns1 ip addr add 20.0.0.2/24 dev wlan1

  sudo ip netns exec ns0 sudo ifconfig wlan0 down
  sudo ip netns exec ns0 sudo iwconfig wlan0 mode monitor
  sudo ip netns exec ns0 sudo ifconfig wlan0 up
  sudo ip netns exec ns0 ifconfig wlan0
  sudo ip netns exec ns1 sudo ifconfig wlan1
  sudo ip netns exec ns1 sudo ifconfig wlan1 down
  sudo ip netns exec ns1 sudo iwconfig wlan1 mode monitor
  sudo ip netns exec ns1 sudo ifconfig wlan1 up
  sudo ip netns exec ns1 ifconfig wlan1
  ```

  ## Additional commands
  sudo rfkill unblock wifi; sudo rfkill unblock all

  ## Launching hostpad and wpa_supplicant
   In namespace-0
  * sudo  hostapd -B -f hostapd.log -i wlan0 [hostapd.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/80211_hw_sim/configuration_files/hostpad_running_config)

   In namespace-1
*  wpa_supplicant -Dnl80211 -iwlan1 -c [./wpa_supplicant.conf](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/80211_hw_sim/configuration_files/wpa_supplicant_running_config) -dd    
