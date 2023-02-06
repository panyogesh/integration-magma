# Install and sample go-diameter programs

## Install go language
* sudo apt-get update
* sudo apt-get -y upgrade
* wget  https://go.dev/dl/go1.19.linux-amd64.tar.gz
* sudo tar -xvf go1.19.linux-amd64.tar.gz
* sudo mv go /usr/local
* sudo mkdir $HOME/GO_PROJECTS
* Add following lines in profile
   ```
   export GOROOT=/usr/local/go
   export GOPATH=/home/vagrant/GO_PROJECTS
   PATH=$GOPATH/bin:$GOROOT/bin:$PATH
   ```
* source ~/.profile

## Get the package for go-diameter
* git clone https://github.com/fiorix/go-diameter.git
* cd go-diameter/

## Run the go-diameter client/server program

### Run the server program
[TERMINAL-1]$ source ~/.profile
[TERMINAL-1]$ export GO111MODULE=on
[TERMINAL-1]$ cd go-diameter/
[TERMINAL-1]$ go run github.com/fiorix/go-diameter/v4/examples/server

### Run the go-diameter client program
[TERMINAL-2]$ source ~/.profile
[TERMINAL-2]$ export GO111MODULE=on
[TERMINAL-2]$ cd go-diameter/
go run github.com/fiorix/go-diameter/v4/examples/client -hello


### Verification logs
```
Hello-Message-Request (HMR)
{Code:111,Flags:0x80,Version:0x1,Length:136,ApplicationId:999,HopByHopId:0xfc180d91,EndToEndId:0xfd8fc8bd}
        Session-Id {Code:263,Flags:0x40,Length:28,VendorId:0,Value:UTF8String{session;1651430902},Padding:2}
        Origin-Host {Code:264,Flags:0x40,Length:16,VendorId:0,Value:DiameterIdentity{client},Padding:2}
        Origin-Realm {Code:296,Flags:0x40,Length:20,VendorId:0,Value:DiameterIdentity{go-diameter},Padding:1}
        Destination-Realm {Code:283,Flags:0x40,Length:20,VendorId:0,Value:DiameterIdentity{go-diameter},Padding:1}
        Destination-Host {Code:293,Flags:0x40,Length:16,VendorId:0,Value:DiameterIdentity{server},Padding:2}
        User-Name {Code:1,Flags:0x40,Length:16,VendorId:0,Value:UTF8String{foobar},Padding:2}
2023/02/06 10:00:50 Received HMA from 127.0.0.1:3868
Hello-Message-Answer (HMA)
{Code:111,Flags:0x0,Version:0x1,Length:132,ApplicationId:999,HopByHopId:0xfc180d91,EndToEndId:0xfd8fc8bd}
        Result-Code {Code:268,Flags:0x40,Length:12,VendorId:0,Value:Unsigned32{2001}}
        Session-Id {Code:263,Flags:0x40,Length:28,VendorId:0,Value:UTF8String{session;1651430902},Padding:2}
        Origin-Host {Code:264,Flags:0x40,Length:16,VendorId:0,Value:DiameterIdentity{server},Padding:2}
        Origin-Realm {Code:296,Flags:0x40,Length:20,VendorId:0,Value:DiameterIdentity{go-diameter},Padding:1}
        Destination-Realm {Code:283,Flags:0x40,Length:20,VendorId:0,Value:DiameterIdentity{go-diameter},Padding:1}
        Destination-Host {Code:293,Flags:0x40,Length:16,VendorId:0,Value:DiameterIdentity{client},Padding:2}
vagrant@oai-gnb-ue-sim:~/go-diameter$
```


## Run the go-diameter s6a_client/s6a_server program

* Running s6a_server
``` go run github.com/fiorix/go-diameter/v4/examples/s6a_server```

* Running s6a_client
``` go run github.com/fiorix/go-diameter/v4/examples/s6a_client -addr 127.0.0.1:3868 -network_type tcp```

* S6a Client/Server Logs
``` 
Authentication-Information-Request (AIR) ...
Authentication-Information-Answer (AIA) ...
2023/02/06 10:21:35 Unmarshaled Authentication-Information Answer:
main.AIA{SessionID:"session;3475979806", ResultCode:0x7d1, OriginHost:"server", OriginRealm:"go-diameter", AuthSessionState:"", ExperimentalResult:main.ExperimentalResult{ExperimentalResultCode:0x0}, AIs:[]main.AuthenticationInfo{main.AuthenticationInfo{EUtranVector:main.EUtranVector{RAND:"\x94\xbf/T\xc3v\xf3\x0e\x87\x83\x06k'\x18Z\x19", XRES:"F\xf0\"\xb9%#\xf58", AUTN:"\xc7G!;\xad~\x80\x00)\bo%\x11\fP_", KASME:"\xbf\x00\xf9\x80h3\"\x0e\xa1\x1c\xfa\x93\x03@\xd6\xf8\x02\xd51Y\xebĝ=\t\x14{\xeb!\xec\xcb:"}}}}
2023/02/06 10:21:35
Sending ULR to 127.0.0.1:3868
Update-Location-Request (ULR) ...
Update-Location-Answer (ULA) ...
2023/02/06 10:21:35 Unmarshaled UL Answer:
```

## Run the test on s6a_proxy and s6a_server
* go-diameter/examples/s6a_proxy/service/test
* go test

   ```ok      github.com/fiorix/go-diameter/v4/examples/s6a_proxy/service/test        0.546s```
