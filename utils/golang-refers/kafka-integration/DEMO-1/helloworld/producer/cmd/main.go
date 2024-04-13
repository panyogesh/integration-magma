package main

import (
	kafkaConfig "helloworld/config"
	"helloworld/producer"
)

func main() {

	topic := kafkaConfig.CONST_TOPIC
	producer.Produce(topic, 20)
}
