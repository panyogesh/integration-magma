# Unit testing framework

## Install pre-requisites

### Install dockers

Refrence : https://docs.docker.com/engine/install/ubuntu/
* sudo apt-get update
* sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
    
* sudo mkdir -m 0755 -p /etc/apt/keyrings
* curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
* echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
* sudo apt-get update
* sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

### Install go language
sudo apt install golang-go

## Verify the packages

* Verifying dockers
```
vagrant@ubuntu-jammy:~/magma/orc8r/cloud/test-results$ sudo docker version
Client: Docker Engine - Community
 Version:           23.0.1
 API version:       1.42
 Go version:        go1.19.5
 Git commit:        a5ee5b1
 Built:             Thu Feb  9 19:47:01 2023
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          23.0.1
  API version:      1.42 (minimum version 1.12)
  Go version:       go1.19.5
  Git commit:       bc3805a
  Built:            Thu Feb  9 19:47:01 2023
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.6.18
  GitCommit:        2456e983eb9e37e47538f59ea18f2043c9a73640
 runc:
  Version:          1.1.4
  GitCommit:        v1.1.4-0-g5fd4c4d
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
vagrant@ubuntu-jammy:~/magma/orc8r/cloud/test-results$
```

* Verifying go language
```
vagrant@ubuntu-jammy:~/magma/orc8r/cloud/test-results$ go version
go version go1.18.1 linux/amd64
vagrant@ubuntu-jammy:~/magma/orc8r/cloud/test-results$
```

## Checkout the code 
git clone https://github.com/magma/magma.git

## Execute the Unit test
* cd magma/orc8r/cloud/docker/
* sudo PWD=$PWD ./build.py --test

## Additional Information

* Results : vim ~magma/cloud/test-results/_src_magma_lte_cloud_go.xml

* Directory for tests
```
  cd magma/cloud/go/services/obsidian/access/tests
  ./cloud/go/services/obsidian/tests
  ./lib/go/protos/tests
```
