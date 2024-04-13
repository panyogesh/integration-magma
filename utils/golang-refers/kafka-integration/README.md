# This proof of concept is to integrate kafka with golang

## Pre-requisites
   * docker and docker-compose

## References

### DEMO-1
* [link](https://levelup.gitconnected.com/introduction-to-kafka-in-go-2a5755df504c)
* [Github code](https://github.com/RyoKusnadi/GoKafka/tree/main/%5B01%5D%20Hello%20World)

## Steps
### DEMO-1

#### Bring up the docker-compose
* cd DEMO-1
* docker-compose up -d

#### Bring up the go program

* cd DEMO-1/helloworld
* go mod init helloworld

#### [TERMINAL-1]
go run consumer/cmd/main.go

#### [TERMINAL-2]
go run producer/cmd/main.go


## Test Logs
```
2024/04/13 09:33:18 [producer] partition id: 0, offset: 20, value: 1713000798415300784
2024/04/13 09:33:18 [producer] partition id: 0, offset: 21, value: 1713000798422602145
2024/04/13 09:33:18 [producer] partition id: 0, offset: 22, value: 1713000798427181257

2024/04/13 09:33:18 [Consumer] partitionid: 0, offset: 20, value: 1713000798415300784
2024/04/13 09:33:18 [Consumer] partitionid: 0, offset: 21, value: 1713000798422602145
2024/04/13 09:33:18 [Consumer] partitionid: 0, offset: 22, value: 1713000798427181257
```
