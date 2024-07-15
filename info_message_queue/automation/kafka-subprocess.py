import subprocess
import threading
import time

def kafka_producer(topic, message, pod_name='my-release-kafka-client', namespace='default'):
    command = [
        'kubectl', 'exec', '--tty', '-i', pod_name, '--namespace', namespace, '--',
        'kafka-console-producer.sh',
        '--broker-list', 'localhost:9092',
        '--topic', topic
    ]
    producer = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = producer.communicate(input=message.encode())
    
    if producer.returncode != 0:
        print(f"Error producing message: {stderr.decode()}")
    else:
        print(f"Produced message: {message}")

def kafka_consumer(topic, pod_name='my-release-kafka-client', namespace='default'):
    command = [
        'kubectl', 'exec', '--tty', '-i', pod_name, '--namespace', namespace, '--',
        'kafka-console-consumer.sh',
        '--bootstrap-server', 'localhost:9092',
        '--topic', topic,
        '--from-beginning'
    ]
    consumer = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            output = consumer.stdout.readline()
            if output == b'' and consumer.poll() is not None:
                break
            if output:
                print(f"Consumed message: {output.decode().strip()}")
    except KeyboardInterrupt:
        consumer.terminate()
        consumer.wait()
    
    stderr = consumer.stderr.read()
    if consumer.returncode != 0:
        print(f"Error consuming messages: {stderr.decode()}")

def start_producer():
    topic = 'test-topic'
    messages = ["Hello, Kafka!", "Another message", "Last message"]
    for message in messages:
        kafka_producer(topic, message)
        time.sleep(1)

def start_consumer():
    topic = 'test-topic'
    kafka_consumer(topic)

if __name__ == '__main__':
    # Start consumer thread
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()

    # Give some time for the consumer to start
    time.sleep(2)

    # Start producer
    start_producer()

    # Wait for the consumer thread to finish
    consumer_thread.join()
