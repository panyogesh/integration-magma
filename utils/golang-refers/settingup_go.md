# Setting up Golang Env

## Reference: 
https://gist.github.com/sathiyaseelan/529695891e290991573d278a56180535

## Steps:
* Set the enviornment variable and download golang
```
sudo rm -rf /usr/bin/go
VERSION="1.19.8"
ARCH="amd64" # go archicture
curl -O -L "https://golang.org/dl/go${VERSION}.linux-${ARCH}.tar.gz"
wget -L "https://golang.org/dl/go${VERSION}.linux-${ARCH}.tar.gz"
tar -xf "go${VERSION}.linux-${ARCH}.tar.gz"
sudo mv -v go /usr/local
```

* Create Directories and update profiles
```
export GOPATH=$HOME/go
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
mkdir -p $GOPATH/src
mkdir -p $GOPATH/bin
mkdir -p $GOPATH/pkg
mkdir -p $GOPATH/src/github.com

Add line in ~/.profile
export GOPATH=$HOME/go
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
source .profile
```

* Set the build directory
```
mkdir radpoc
cd radpoc/
go mod init projrad
go get -u layeh.com/radius

vagrant@distro-magma:~/radpoc$ ls
go.mod  go.sum  rad-client.go
vagrant@distro-magma:~/radpoc$
```
