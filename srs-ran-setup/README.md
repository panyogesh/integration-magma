# Setup for srs-ran

## Build the docker images
* sudo docker build -t srsran:jan07 .

## Run the docker image
* sudo docker run --rm --cap-add=NET_ADMIN --device /dev/net/tun -it --entrypoint bash srsranlocal:jan07
