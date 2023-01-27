# Docker tips/tricks

## Executing on local host
* docker run -ti --privileged --net=host --pid=host --ipc=host --volume /:/host busybox chroot /host
* sudo docker run -ti --privileged --net=host --pid=host --ipc=host --volume /:/host ubuntu:20.04 chroot /host /bin/bash
