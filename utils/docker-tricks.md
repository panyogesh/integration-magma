# Docker tips/tricks

## Executing on local host
* docker run -ti --privileged --net=host --pid=host --ipc=host --volume /:/host busybox chroot /host
* sudo docker run -ti --privileged --net=host --pid=host --ipc=host --volume /:/host ubuntu:20.04 chroot /host /bin/bash

## Clean up docker scripts
```
sudo docker container stop $(sudo docker container ls -aq)
sudo docker container rm $(sudo docker container ls -aq)
sudo docker container prune
sudo docker image prune -a
sudo docker volume prune
sudo docker system prune -a
sudo docker system prune```
