# Steps for installing kind 
* Refer: https://kind.sigs.k8s.io/docs/user/quick-start/#installation

## Option 1:
```
# For AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
# For ARM64
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-arm64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

## Option 2:
* wget --no-check-certificate https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
* chmod +x kind-linux-amd64
* sudo ./kind-linux-amd64 create cluster
* sudo kubectl get nodes


