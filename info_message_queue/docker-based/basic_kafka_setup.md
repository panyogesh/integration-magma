# Document covers the basic kafka bring up and steps to verify the setup

## Steps to bring up the docker image
* Use docker-compose.yml to bring up kafka server
* From the docker contanier execute the following three commands
    - docker exec -it <kafka_container_id_or_name> /bin/bash
    - Create topic branch : ```kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1```
    - Create producer: ```kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092```
    - Create consumer: kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --from-beginning```

## Execution steps
* sudo docker-compose up -d
* **[Terminal-1]**:docker exec -it <kafka_container_id_or_name> /bin/bash
* **[Terminal-1]**: kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
* **[Terminal-1]**: kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092
* **[Terminal-2]**: kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --from-beginning






