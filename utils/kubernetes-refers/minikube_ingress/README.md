# This example is to show the minikubes ingress functionality

## Pre-Requisites
* minikube
* docker
* Linux with desktop version (sudo apt install slim) [Ref-slim](https://phoenixnap.com/kb/how-to-install-a-gui-on-ubuntu)

## Steps for the configuration
* Start the minikube
``` minikube start```
* Start the ingress on minikube
```
minikube addons enable ingress
kubectl get pods -n ingress-nginx
```
* Create the web-app with NodePort service:- 
  kubectl apply -f [example-web-deployment.yaml](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/kubernetes-refers/minikube_ingress/example-web-deployment.yaml)
  
   
* Create the ingress services :- 
  kubectl apply -f [example-web-ingress.yaml](https://raw.githubusercontent.com/panyogesh/integration-magma/main/utils/kubernetes-refers/minikube_ingress/example-web-ingress.yaml)
  
  ## Steps to verify
  ```curl --resolve "hello-world.info:80:$( minikube ip )" -i http://hello-world.info```

