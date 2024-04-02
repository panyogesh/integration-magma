# Example shows the basic Kubernetes steps for getting started

## Sample Kubernetes Deployment

* cat nginx-deployment.yml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 8080
```
* cat nginx-service.yml
```
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

## Commands for deployment
* kubectl apply -f nginx-deployment.yml
* kubectl apply -f nginx-service.yml

## Steps to validate
* kubectl describe service nginx-service
* 
