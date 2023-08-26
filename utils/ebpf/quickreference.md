# This document for the ebpf using python Quick How to Guide

## Package installation
* sudo apt install python3-pip
* pip install bcc
* pip install pytest
* sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
* sudo python3.8 helloWorld.py
```
https://github.com/lizrice/ebpf-beginners/blob/main/hello.py
```
From other terminal do some operations.

## C code installation for EBPF
### Installing CLANG tool
* sudo apt install clang

### Installing libbpf
* Following are specific to ubuntu 22.0.4  
  * sudo apt install pkg-config
  * sudo apt install build-essential
  * sudo apt install libelf-dev

* git clone --depth 1 https://github.com/libbpf/libbpf
* cd libbpf/src/
* sudo make install

### Installing bpftools
* sudo apt update && sudo apt install -y git
* git clone --recurse-submodules https://github.com/libbpf/bpftool.git
* cd bpftool/src
* sudo ln -s /usr/bin/llvm-strip-14 /usr/bin/llvm-strip
* make
* sudo make install
*  bpftool

Sample code : learning-ebpf/chapter3

## Quick Notes on EBPF
### Compiling BPF files
hello.bpf.o: %.o: %.c clang -target bpf -I/usr/include/$(shell uname -m)-linux-gnu -g -O2 -c $< -o $@

### Inspect BPF files
llvm-objdump -S hello.bpf.o

### Cheat Sheet
* sudo bpftool prog load hello.bpf.o /sys/fs/bpf/hello  ```Load the hello program in kernel```
* sudo ls /sys/fs/bpf                                   ```To check the loaded program```
* sudo bpftool prog list                                ```Inspect the loaded program```
                                                        ```Every loded program has been assigned the ID```
                                                      ```Use this command to get the ID```
* sudo bpftool prog show id 540 --pretty                ```Certain information about the program```
* sudo bpftool prog dump xlated name hello              ```Translated bytecode```
* sudo bpftool net attach xdp id 111 dev enp0s3         ```Attach the program with interface```

* sudo ip link set dev eth0 xdp obj hello.bpf.o sec xdp ```Otherways of attaching```
* sudo ip link set dev eth0 xdp off

* sudo bpftool net list                                 ```To see the attached interface```
* sudo cat /sys/kernel/debug/tracing/trace_pipe         ```for checking the packet output```
* sudo bpftool prog tracelog                            ```Tracing the contents```
* sudo bpftool map list                                 ```Maps loaded in the kernel```
* sudo bpftool map dump name hello.bss                  ```To access global variables```
* sudo bpftool net detach xdp dev enp0s3                ```Detach the program from the interface```
* sudo  rm /sys/fs/bpf/hello                            ```Remove the program from the kernel```








