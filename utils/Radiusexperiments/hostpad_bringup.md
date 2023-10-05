# Steps for compiling hostapd

## Fetch the tar from the release directory
https://w1.fi/releases/hostapd-2.10.tar.gz

## Configure and Compile
### Install packages
sudo apt install libnl-3-dev libssl-dev libnl-genl-3-dev libdbus-1-dev isc-dhcp-server iptables-persistent

### Compile & Install
* With default Config
  ```
  cd hostapd-2.9/hostapd
   cp defconfig .config
   vim .config
   make
   make install
   ```

  * Additional config
    [link](https://github.com/panyogesh/integration-magma/blob/main/utils/Radiusexperiments/80211_hw_sim/configuration_files/hostapd_compile_config)

## Reference
https://hackmd.io/@akiranet/ByhNQ7aGv
