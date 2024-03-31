# This section is to install minikube on top of ubuntu 22.0.4

## Install Dockers
* sudo apt update
* sudo apt install docker.io
* sudo systemctl start docker
* sudo systemctl enable docker
* sudo usermod -aG docker $USER && newgrp docker

## Install Kubectl
### With Snap
* sudo snap install kubectl --classic
* kubectl version --client

### Download as binary
* sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg
* curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

### Make it Executable
* chmod +x ./kubectl
* sudo mv ./kubectl /usr/local/bin/kubectl
* kubectl version --client

## Install minikube
* curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
* sudo install minikube-linux-amd64 /usr/local/bin/minikube

## Bringing up Minikube
* minikube start
* kubectl get nodes
```
vagrant@ebpf-test:~$ kubectl get nodes
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   7h1m   v1.28.3
vagrant@ebpf-test:~$
```
