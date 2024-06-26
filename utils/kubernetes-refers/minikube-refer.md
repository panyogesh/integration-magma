# This section is to install & experiment minikube on top of ubuntu 22.0.4

## Refrences
* [Techworld with Nana Kubernetes](https://www.youtube.com/watch?v=X48VuDVv0do)
* [Kubernetes Refrences](https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/)

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

## External Connectivity to minikube cluster
Windows (HOST) (192.168.99.1)---> (192.168.99.199)Virtual-Box: VM(ubuntu-22.0.4) ---> minikube (ip:192.168.49.2)

* Add a route from  Windows to Linux directed towards the minikube. [Ref](https://www.youtube.com/watch?v=5z3uXrFxN1k)
  ``` 
  route ADD 192.168.49.0 MASK 255.255.255.0 192.168.99.199
  ```
* Allow packet to be accepted by iptables for DOCKER_USER [Ref](https://serverfault.com/questions/1005648/docker-changes-iptables-forward-policy-to-drop)
  ```
  iptables -I DOCKER-USER -j ACCEPT 
  ```

 ## Login and Password for mongo-express
 admin / pass [Ref](https://stackoverflow.com/questions/77559161/why-does-the-mongo-express-service-external-service-in-my-browser-require-a-user#:~:text=You%20need%20to%20enter%20credentials,in%20mongo%2Dexpress%20documentation%20here.)

## Connecting minkube dashboard runninng inside VM from Windows host on same subnet
Windows (HOST) (192.168.99.1)---> (192.168.99.199)Virtual-Box: VM(ubuntu-22.0.4) ---> minikube (ip:192.168.49.2)

Terminal-1
```
vagrant@ubuntu-jammy:~/KubernetesProgram/IngressExample$  minikube dashboard --url
* Verifying dashboard health ...
* Launching proxy ...
* Verifying proxy health ...
http://127.0.0.1:39505/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```
Terminal-2
```
kubectl proxy --address='0.0.0.0' --disable-filter=true
```

Terminal-3
```
sudo apt install firewalld
sudo firewall-cmd --zone=public --add-port=8001/tcp --permanent
sudo firewall-cmd --reload
```

Access : 
http://192.168.99.199:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
