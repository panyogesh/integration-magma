# Quick refernce to production level orchestrator

## Log Collection
### Script for collecting logs from all orchestrator
```
#!/usr/bin/env bash

DEPLOYMENT=orc8r

for p in $(kubectl get pods | grep ^${DEPLOYMENT}- | cut -f 1 -d ' '); do
    echo ---------------------------
    echo $p
    echo ---------------------------
    #kubectl logs $p | grep -v error
    kubectl logs $p
done
```

## Quick Steps to install production level orchestration
* Refernce : https://github.com/magma/magma/blob/master/docs/readmes/orc8r/deploy_using_ansible.md
* Steps 
   - sudo bash -c "$(curl -sL https://github.com/magma/magma-deployer/raw/main/deploy-orc8r.sh)"
   - sudo su - magma
   - kubectl get pods
   - cd ~/magma-deployer
   - ansible-playbook config-orc8r.yml

## Curl Command Examples
* Reference : https://github.com/ShubhamTatvamasi/magma-curl
* Steps
    - Follow the steps mentioned above for installing production level orchestrator
    - Got secrets : cd magma-deployer/secrets
    - Execute the following command : 
      ```
      curl  -k --cert ./admin_operator.pem --key admin_operator.key.pem -X 'GET'   'https://api.magma.local/magma/v1/tenants'   -H 'accept: application/json'
      []

      curl  -k --cert ./admin_operator.pem --key admin_operator.key.pem -X 'GET'      
        'https://172.16.4.38:9443/magma/v1/tenants'   -H 'accept: application/json'
     
      curl  -k --cert ./admin_operator.pem --key admin_operator.key.pem -X 'GET'   
       'https://172.16.4.38:9443/magma/v1/lte/test/subscribers/IMSI001011234567430'   -H 'accept: application/json'

      ```
## References
https://wiki.magmacore.org/display/HOME/2023-03-09+Meeting
