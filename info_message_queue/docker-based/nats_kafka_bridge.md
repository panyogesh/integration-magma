# This document is to show the nats-kafka bridge deployment 

## Toplogy
Kafka-Producer === nats-kafka-bridge === nats-subscriber

## Nats-Kafka Configuration
[Conf-File](https://github.com/nats-io/nats-kafka/blob/main/conf/nats-kafka.conf)

## Steps for setup
* Bring up the docker-compose
* Bring up kafka and nats using the [docker-compose](https://github.com/panyogesh/integration-magma/blob/main/info_message_queue/docker-based/docker-compose.yml)
* Start the nats-kafa with default configuration file
* From Kafka-producer send the message towards nats subscriber

## Steps to compile nats-kafka
* git clone https://github.com/nats-io/nats-kafka.git
* cd nats-kafka
* make nats-kafka.docker
* nats-kafka.docker -c conf/nats-kafka.conf

## Overall execution
### Bring up docker-compse with nats and kafka
* sudo docker-compose up -d
  
### Bring up nats-kafka server
* nats-kafka.docker -c conf/nats-kafka.conf

### Bring up nats subscriber
* nats sub kafka.events

### Login to the Kafka docker and send the message
* docker exec -it $(sudo docker ps | grep "bitnami/kafka:latest"  | awk '{print $1}') /bin/bash
*  kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events

### Output
```
 kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events
#
>>^[[1;5C
>hi
>

agrant@ubuntu-jammy:~/kafka/nats-kafka$ nats sub kafka.events
11:01:32 Subscribing on kafka.events

[#1] Received on "kafka.events"
nil body
[#2] Received on "kafka.events"
[#3] Received on "kafka.events"
hi
```

  
