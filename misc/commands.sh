# Initialize Poetry
pip3 install pipx; pipx ensurepath; source ~/.bashrc; pipx install poetry; poetry install; poetry shell

# Delete a kafka topic
docker exec -it broker kafka-topics --bootstrap-server broker:9092 --delete --topic ip_addresses_by_countries

# List kafka topics
docker exec -it broker kafka-topics --bootstrap-server broker:9092 --list

# Describe a topic
docker exec -it broker kafka-topics --bootstrap-server broker:9092 --describe --topic ip_addresses_by_countries

# Write topic content to file
docker exec -it broker kafka-console-consumer --bootstrap-server broker:9092 --topic ip_addresses_by_location --from-beginning > output.txt