# Setup for srs-ran

## Build the docker images
* sudo docker build -t srsran:jan07 .

## Launch the docker image
* sudo docker run  --name srsransim-app -it --cap-add=NET_ADMIN --device /dev/net/tun --privileged --rm srsranlocal:jan07 /bin/bash
* sudo docker exec -it srsransim-app

## Launch the srsen and srsue binaries
- srsenb
- srsue ~/.config/srsran/ue.conf

## Additional configuation
ip route add 8.8.8.8/32 dev <tun_srsue_ip>
ping 8.8.8.8 -I <tun_srsue_ip>
