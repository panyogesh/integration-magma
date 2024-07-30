from confluent_kafka import Producer

def kafka_producer(broker, topic, messages):
    producer = Producer({'bootstrap.servers': broker})
    
    def delivery_report(err, msg):
        if err:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    for message in messages:
        producer.produce(topic, message, callback=delivery_report)
        producer.poll(0)

    producer.flush()

from confluent_kafka import Consumer, KafkaError

def kafka_consumer(broker, group, topic, timeout=5.0):
    consumer = Consumer({
        'bootstrap.servers': broker,
        'group.id': group,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([topic])
    messages = []

    while True:
        msg = consumer.poll(timeout)
        if msg is None:
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                break
            else:
                print(msg.error())
                break
        messages.append(msg.value().decode('utf-8'))

    consumer.close()
    return messages

import pytest

@pytest.fixture
def kafka_config():
    return {
        'broker': 'localhost:9092',
        'topic': 'test_topic',
        'group': 'test_group'
    }

def test_kafka_producer_consumer(kafka_config):
    broker = kafka_config['broker']
    topic = kafka_config['topic']
    group = kafka_config['group']
    
    messages_to_send = ["msg1", "msg2", "msg3"]

    # Produce messages
    kafka_producer(broker, topic, messages_to_send)

    # Consume messages
    consumed_messages = kafka_consumer(broker, group, topic)

    assert consumed_messages == messages_to_send
