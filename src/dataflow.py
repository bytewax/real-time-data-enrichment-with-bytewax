from bytewax import Dataflow, spawn_cluster, AdvanceTo, Emit
from kafka import KafkaProducer, KafkaConsumer
import requests
import json

producer = KafkaProducer(value_serializer=lambda m: json.dumps(
    m).encode('ascii'), bootstrap_servers='localhost:9092')


def input_builder(worker_index, total_workers):
    consumer = KafkaConsumer(
        'ip_addresses_by_countries',
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset='earliest'
    )
    epoch = 0
    for message in consumer:
        ip_address = message.value.decode('ascii')
        yield Emit(ip_address)
        epoch += 1
        yield AdvanceTo(epoch)


def output_builder(worker_index, worker_count):
    def send_to_kafka(previous_feed):
        location_json = previous_feed[1]
        producer.send('ip_addresses_by_location', key=f"{location_json['country_name']}".encode('ascii'), value=location_json)

    return send_to_kafka

def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/')
    response_json = response.json()
    location_data = {
        "ip": ip_address,
        "city": response_json.get("city"),
        "region": response_json.get("region"),
        "country_name": response_json.get("country_name")
    }
    return location_data

flow = Dataflow()
flow.map(get_location)
flow.capture()

if __name__ == "__main__":
    spawn_cluster(flow, input_builder, output_builder, worker_count_per_proc=1)
