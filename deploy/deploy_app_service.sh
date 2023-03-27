#!/bin/bash
cd /home/ryan/projects/JapaneseMessagingCode

docker stop $(docker ps -q --filter ancestor=message-bot )

docker build -t message-bot .

docker run message-bot
