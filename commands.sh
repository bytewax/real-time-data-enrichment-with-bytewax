# Create Kafka topic with 20 partitions
rpk topic create -p 20 user_ip_addresses_and_countries

# Number of Partitions = Desired Throughput / Partition Speed

# Delete a kafka topic
docker exec -it broker kafka-topics --bootstrap-server broker:9092 --delete --topic ip_addresses_by_countries

# List kafka topics
docker exec -it broker kafka-topics --bootstrap-server broker:9092 --list

# Describe a topic
docker exec -it broker kafka-topics --bootstrap-server broker:9092 --describe --topic ip_addresses_by_countries
