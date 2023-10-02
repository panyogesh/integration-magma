# Enabling mac80211_hwsim in linux kernel

## Check whether the kernel is compiled with HWSIM
* grep HWSIM /boot/config-*
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

  ## References
  https://askubuntu.com/questions/1265137/avoid-missing-kernel-linux-modules-extra-xx-generic-when-updating-kernel
