# Learnings from DPDK

### DPDK Installation
---

#### Update System
---
* sudo apt update
* sudo apt install -y build-essential pkg-config libnuma-dev python3-pyelftools
* sudo apt install -y meson ninja-build

 
#### Install additional dependencies (optional) 
---
sudo apt install -y linux-headers-$(uname -r)

 
#### Download and Build DPDK
---
```
wget https://fast.dpdk.org/rel/dpdk-22.11.tar.xz
tar xf dpdk-22.11.tar.xz
cd dpdk-22.11
meson setup build
cd build
ninja
sudo ninja install
sudo ldconfig
```

 
#### Set Huge Pages
---
**Reserve hugepages (adjust count as needed)**

```echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages```

**Mount hugepage filesystem**
```
sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs nodev /mnt/huge
```

**Make persistent (add to /etc/fstab)**
- echo "nodev /mnt/huge hugetlbfs defaults 0 0" | sudo tee -a /etc/fstab
 
 
#### Compiling & Running the code
---
##### Code layout
- primary_process.c
- secondary_process.c
- Makefile

##### Compiling the code
* make
 
##### Running the code
* echo 1024 | sudo tee /proc/sys/vm/nr_hugepages (do this if something failes)
* sudo ./primary_process --file-prefix=multi --proc-type=primary --socket-mem=1024
* sudo ./secondary_process --file-prefix=multi --proc-type=secondary --socket-mem=1024


##### Additional Clean ups
* sudo rm -rf /var/run/dpdk/* /run/user/*/dpdk

 
##### DPDK Telemetry / Runtime Socket Debugging (v20.11+)
* sudo socat - UNIX-CONNECT:/var/run/dpdk/rte/telemetry
