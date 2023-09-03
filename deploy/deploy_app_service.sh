#!/bin/bash
cd /home/ryan/projects/JapaneseMessagingCode

docker stop $(docker ps -q --filter ancestor=message-bot )

echo "creating database..."
docker run -d -p 8529:8529 -e ARANGO_ROOT_PASSWORD=openSesame arangodb/arangodb:3.11.0
echo "database creation complete"

echo "generating bot docker"
docker build -t message-bot .
docker run -d message-bot
echo "bot docker generation complete"

sleep 10

python3 .\move_vals_from_exl_to_arango.py -j /tmp/config.json -c