from bytewax import Dataflow, spawn_cluster, AdvanceTo, Emit
from bytewax.testing import doctest_ctx
from kafka import KafkaProducer, KafkaConsumer
import requests
import json

producer = KafkaProducer(value_serializer=lambda m: json.dumps(
    m).encode('ascii'), bootstrap_servers='localhost:9092')


def input_builder(worker_index, total_workers):
    consumer = KafkaConsumer(
        'user_ip_addresses_and_countries',
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset='earliest'
    )
    for message in consumer:
        ip_address = json.loads(message.value)
        yield ip_address


def output_builder(worker_index, worker_count):
    return print

def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/200.34.24.56/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country_name": response.get("country_name")
    }
    return location_data


def save_location_to_kafka(location_json):
    producer.send('user_ip_addresses_by_locations', key=f"{location_json['country_name']}".encode(
        'ascii'), value=location_json)

flow = Dataflow()
flow.map(get_location)
flow.map(save_location_to_kafka)
flow = Dataflow()
flow.capture()

spawn_cluster(flow, input_builder, output_builder, worker_count_per_proc=20)
