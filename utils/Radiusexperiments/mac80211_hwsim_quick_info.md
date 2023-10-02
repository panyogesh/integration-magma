# Enabling mac80211_hwsim in linux kernel

## Check whether the kernel is compiled with HWSIM
* sudo apt install   wireless-tools
* grep HWSIM /boot/config-*
* sudo apt install linux-generic
* sudo modprobe mac80211_hwsim or sudo modprobe mac80211_hwsim radios=2 dyndbg=+p
  ```
  vagrant@exp-2004-ubuntu:/lib/modules/5.4.0-163-generic$ lsmod | grep mac
     mac80211_hwsim         61440  0
     mac80211              847872  1 mac80211_hwsim
     cfg80211              708608  2 mac80211_hwsim,mac80211
     libarc4                16384  1 mac80211
  vagrant@exp-2004-ubuntu:/lib/modules/5.4.0-163-generic$
  ```

## Configuration Check
* sudo iw list
* sudo iw dev
```
vagrant@exp-2004-ubuntu:~/TMP/hostapd-2.10/hostapd$ sudo iw dev
phy#1
        Unnamed/non-netdev interface
                wdev 0x100000002
                addr 42:00:00:00:01:00
                type P2P-device
                txpower 20.00 dBm
        Interface wlan1
                ifindex 8
                wdev 0x100000001
                addr 02:00:00:00:01:00
                type managed
                txpower 20.00 dBm
phy#0
        Interface wlan0
                ifindex 7
                wdev 0x1
                addr 02:00:00:00:00:00
                type managed
                txpower 20.00 dBm
```

* sudo apt install iw
  
## References
- https://askubuntu.com/questions/1265137/avoid-missing-kernel-linux-modules-extra-xx-generic-when-updating-kernel
- https://github.com/sysprog21/vwifi
- https://hackmd.io/@akiranet/r1OC8CaNv#hwsim-on-OpenWrt
