## Saturn

* Use the patch
* Create Magma VM..it will fail
* vagrant ssh magma
* cd magma/lte/gateway 
* sudo mv /etc/apt/sources.list.d/magma.list ~
* sudo apt-add-repository ppa:ansible/ansible
* sudo apt update
* sudo apt install ansible
* execute the command : ansible-playbook --extra-vars=ansible_ssh_user\=\'vagrant\' --limit="magma" --inventory-file=deploy/hosts -v --timeout=30 deploy/magma_dev.yml
