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
## Execute uesim testcase

* Folder :magma/cwf/gateway/docker

  ```
  vagrant@radius-exp:~/magma/cwf/gateway/docker$ cat /etc/magma/uesim.yml
  radius_auth_address: "192.168.70.101:1812"
  radius_acct_address: "192.168.70.101:1813"
  radius_secret: "123456"
  amf: "0000"
  subscribers:
      "001011234567890":
          auth_key: "465B5CE8B199B49FAA5F0A2EE238A6BC"
  ```
* go run main.go  add_ue 001011234567890

