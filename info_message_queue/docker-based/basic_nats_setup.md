# Document covers the basic nats bring up and steps to verify the setup

## Steps to bring up the docker image
* used [docker-compose.yml](https://github.com/panyogesh/integration-magma/blob/main/info_message_queue/docker-based/docker-compose.yml) to bring up nats server
* Install nats-cli from https://github.com/nats-io/natscli
   - Command: ```go install github.com/nats-io/natscli/nats@latest```
   - From the host execute the commands:
     * nats sub -s nats://localhost:4222 foo
     * nats pub -s nats://localhost:4222 foo "Hello, NATS!"

## Execution
* sudo docker-compose up -d
* [Terminal-1]: nats sub -s nats://localhost:4222 foo
* [Terminal-2]: nats pub -s nats://localhost:4222 foo "Hello, NATS!"

    

