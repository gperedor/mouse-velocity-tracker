FROM eclipse-temurin:latest

COPY docker/housekeeping/scripts /scripts

# Install Kafka for the CLI utils
RUN cd /tmp/ \
    && apt-get update \
    && apt-get install -y wget \
    && wget https://dlcdn.apache.org/kafka/4.1.0/kafka_2.13-4.1.0.tgz \
    && tar -xzf kafka_2.13-4.1.0.tgz \
    && mv kafka_2.13-4.1.0/ /opt/kafka \
    && rm kafka_2.13-4.1.0.tgz

CMD ["sh", "/scripts/setup-and-startup.sh"]
