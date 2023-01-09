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
- ip route add 8.8.8.8/32 dev <tun_srsue_ip>
- ping 8.8.8.8 -I <tun_srsue_ip>

## Adding subscriber in Magma
- python3.8 subscriber_cli.py  add --lte-auth-key 00112233445566778899aabbccddeeff --lte-auth-opc 63BFA50EE6523365FF14C1F45F88737D IMSI001010123456780
- python3.8 subscriber_cli.py update --lte-auth-key 00112233445566778899aabbccddeeff --lte-auth-opc 63BFA50EE6523365FF14C1F45F88737D --apn-config internet,5,15,1,1,1000,2000,0,,,,  IMSI001010123456780
