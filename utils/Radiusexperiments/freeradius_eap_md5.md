# Test for EAP-MD5 

## Refrences:
https://github.com/theaaf/radius-server/tree/master

## Steps for integration
* sudo docker compose up --build radius-test
* sudo docker compose run radius-server add-identity --name user --password password --redis redis:6379
* Test: radtest -4 -t eap-md5 -x 'user' 'password' 127.0.0.1 10 'secret'

## Pcap Snapshot
![image](https://github.com/panyogesh/integration-magma/assets/69527565/5e13fe4a-5e2c-49b1-b1ed-b37aa7ecde83)

## Sample logs
[eap-md5.zip](https://github.com/panyogesh/integration-magma/files/12726246/eap-md5.zip)
