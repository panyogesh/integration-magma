## Saturn

* Use the patch
* Create Magma VM..it will fail
* vagrant ssh magma
* cd magma/lte/gateway 
* execute the command : ansible-playbook --extra-vars=ansible_ssh_user\=\'vagrant\' --limit="magma" --inventory-file=deploy/hosts -v --timeout=30 deploy/magma_dev.yml
