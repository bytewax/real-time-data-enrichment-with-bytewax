from bytewax import Dataflow, cluster_main, spawn_cluster
from bytewax.inputs import KafkaInputConfig
from kafka import KafkaProducer
import requests
import json

producer = KafkaProducer(value_serializer=lambda m: json.dumps(
    m).encode('ascii'), bootstrap_servers='localhost:9092')


def output_builder(worker_index, worker_count):
    def send_to_kafka(previous_feed):
        location_json = previous_feed[1]
        producer.send('ip_addresses_by_location', key=f"{location_json['country_name']}".encode('ascii'), value=location_json)

    return send_to_kafka


def get_location(data):
    key, value = data
    ip_address = value.decode('ascii')
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
flow.inspect(print)
flow.map(get_location)
flow.inspect(print)
flow.capture()


if __name__ == "__main__":
    input_config = KafkaInputConfig(
        "localhost:9092", "ip_adds", "ip_addresses_by_countries", messages_per_epoch=1
    )
    spawn_cluster(flow, input_config, output_builder)
    # cluster_main(flow, input_config, output_builder, [], 0,)
