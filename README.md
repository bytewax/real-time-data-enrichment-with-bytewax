# Kafka Bytewax Demo
This repo contains a Bytewax dataflow that uses Kafka as input and writes modified data to another Kafka topic. 

## Installation
You will need to install poetry for dependency management. The easiest way is through pipx. You can run the script in ./poetry-initializer-script.sh to install all depdencies and start a poetry shell. Find the script below for reference:

```sh
pip install -r requirements.txt
```


The poetry install command installs Bytewax and Kafka-Python. These depdencies are Python libraries that communicate with Bytewax and Kafka respectively.

## Installing Other Depdencies

You need Kafka to run this dataflow. The easiest way to run Kafka is through the Docker compose file containing Kafka broker and Zookeeper. Navigate to the kafka directory and run the docker compose command using the command below:

```sh
cd kafka
docker compose up -d
```

### Setting up the Kafka topics

This dataflow has two topics of concern:

1. An input topic, ip_addresses_by_countries, that will store ip addresses partitioned by the country of origin name.
2. An output topic, ip_addresses_by_location, that will store JSON data of IP address location data. This includes city, state or region, and country.

Each topic has 20 partitions and will be created using Kafka Python. You can create both by running the initializer.py Python script using the command below:

```sh
python initializer.py
```

The initializer script also produces IP address data into the input topic from the file, `./ip_addresses_with_countries.txt`.

## Running the Dataflow

You can run the dataflow as a normal Python script. Use the command below to run the dataflow:

```sh
python dataflow.py
```

This should source data from the input topic and write it to the output topic.