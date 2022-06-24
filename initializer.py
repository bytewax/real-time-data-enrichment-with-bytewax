from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
from time import sleep
import json
from traceback import format_exc, format_exception

input_topic_name = "ip_addresses_by_countries"
output_topic_name = "ip_addresses_by_location"
localhost_bootstrap_server = "localhost:9092"
producer = KafkaProducer(bootstrap_servers=[localhost_bootstrap_server])
admin = KafkaAdminClient(bootstrap_servers=[localhost_bootstrap_server])

# Create input topic
try:
    input_topic = NewTopic(input_topic_name, num_partitions=20, replication_factor=1)
    admin.create_topics([input_topic])
except:
    print(f"Topic {input_topic_name} already exists")

# Create output topic
try:
    output_topic = NewTopic(output_topic_name, num_partitions=20, replication_factor=1)
    admin.create_topics([output_topic])
except:
    print(f"Topic {output_topic_name} already exists")

try:
    for line in open("ip_addresses_with_countries.txt"):
        ip_address, country_raw = line.split(",")
        country = country_raw[:-1]
        producer.send(input_topic_name, key=f"{country}".encode('ascii'), value=f"{ip_address}".encode('ascii'))
        sleep(0.1)
except KafkaError:
    print("A kafka error occured")