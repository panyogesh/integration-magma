package main

import (
	kafkaConfig "helloworld/config"
	"helloworld/consumer"
)

func main() {

	topic := kafkaConfig.CONST_TOPIC
	consumer.Consume(topic)

}
