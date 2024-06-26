package consumer

import (
	kafkaConfig "helloworld/config"
	"log"

	"github.com/IBM/sarama"
)

func Consume(topic string) {
	config := sarama.NewConfig()

	consumer, err := sarama.NewConsumer([]string{kafkaConfig.CONST_HOST}, config)

	if err != nil {
		log.Fatal("NewConsumer err: ", err)
	}

	defer consumer.Close()

	partitionConsumer, err := consumer.ConsumePartition(topic, 0, sarama.OffsetNewest)

	if err != nil {
		log.Fatal("consumePartion err: ", err)
	}

	defer partitionConsumer.Close()

	for message := range partitionConsumer.Messages() {

		log.Printf("[Consumer] partitionid: %d, offset: %d, value: %s\n",
			message.Partition, message.Offset, message.Value)
	}

}
