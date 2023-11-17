# Place holder for storing all the cwag related information

## Running the unit testcase of cwag
* make -C /home/vagrant/magma/cwf/gateway test
* go test -c  services/uesim/servicers/eap_aka_test.go services/uesim/servicers/eap_test.go
* gdb servicers.test

## Running the Feg Unit tests
* ~/magma/feg/radius/src
* go test ./...

## Brining up cwag
* Apply the patch [link](https://github.com/panyogesh/integration-magma/blob/main/cwag-feat/cwag-basic-bringup.diff)
* Run the following commands
  ```
  sudo docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.integ-test.yml down
  sudo docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.integ-test.yml build
  sudo docker-compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.integ-test.yml up -d
  ```

## gateway.mconfig for generic params
[gateway.mconfig](https://github.com/panyogesh/integration-magma/blob/main/cwag-feat/gateway.mconfig)

## Execute uesim testcase
### Subscriber creation using hss
* [sample-hss.yml](https://github.com/panyogesh/integration-magma/blob/main/cwag-feat/hss.yml)
* Folder :/etc/magma/feg/hss.yml
* Add subscriber
```
cd /home/vagrant/magma/feg/gateway/tools/hss_cli
go run main.go add -subscriber_id 001011234567890 -lte_subscription_active true
go run main.go get -subscriber_id 001011234567890
```

### Testing using uesim
* [sample-uesim.yml](https://github.com/panyogesh/integration-magma/blob/main/cwag-feat/uesim.yml)
* Folder : /etc/magma/
* Path: ``` /home/vagrant/magma/cwf/gateway/tools/uesim_cli/ ```
* Add Subscriber in uesim: ``` go run main.go  add_ue 001011234567890 ```
* Authenticate Subscriber in uesim: ``` go run main.go auth 001011234567890 ```

### Verification using swx_proxy
* go run main.go sar 001011234567890
* go run main.go mar 001011234567890