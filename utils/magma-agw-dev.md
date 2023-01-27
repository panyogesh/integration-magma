# Quick tips for magma-agw dev

* In case if ansible-playbook to be used to install software
```
      +++ b/lte/gateway/deploy/magma_dev.yml
      @@ -14,6 +14,7 @@
      
       - name: Set up Magma dev build environment on a local machine
         hosts: dev
      +  connection: local
         become: yes

sudo apt-get install ansible
sudo rm /etc/apt/sources.list.d/magma.list*
sudo apt -y install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt install ansible

ansible-playbook --extra-vars=ansible_ssh_user\=\'vagrant\' --limit="magma" --inventory-file=deploy/hosts -v --timeout=30 deploy/magma_dev.yml
```
