#!/bin/sh
set -x


# Create Kafka topic
/opt/kafka/bin/kafka-topics.sh --create \
                               --topic ${KAFKA_TOPIC} \
                               --bootstrap-server ${KAFKA_HOST}:${KAFKA_PORT} \
                               --partitions ${KAFKA_TOPIC_PARTITIONS}
