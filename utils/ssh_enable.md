## Enabling SSH Configuration
* /etc/ssh/sshd_config
* PasswordAuthentication -> yes
* ChallengeResponseAuthentication -> no
* sudo systemctl restart sshd

- Reference : https://phoenixnap.com/kb/ssh-permission-denied-publickey

## Script
```
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo service sshd restart
```
