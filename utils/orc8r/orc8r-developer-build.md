# Building Orchestrator

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

## Building & Installing Orchestrator
* cd magma/orc8r/cloud/docker 
* sudo PWD=$PWD ./build.py --all   
* sudo PWD=$PWD ./run.py --metrics 

## Connecting to Swagger
* cd ../../../.cache/test_certs 
* cp admin_operator.pfx ../../../ 
* https://172.16.9.3:9443/swagger/v1/ui 

## Building and Installing NMS
* cd magma/nms
* sudo docker-compose build magmalte  
* sudo docker-compose up -d 
* sudo ./scripts/dev_setup.sh 

## Update the hosts file

* C:\Windows\System32\drivers\etc\hosts 

192.168.56.101 localhost
192.168.56.101 magma-test.localhost
192.168.56.101 magma-test
192.168.56.101 magma-test.magma
192.168.56.101 master.magma.test 
192.168.56.101 host

## Access the NMS
magma-test : https://magma-test/
host : https://host
