import os


def read_config() -> dict[str, str]:
    keys_and_defaults = {
        "KAFKA_HOST": "localhost",
        "KAFKA_PORT": "9092",
        "KAFKA_TOPIC_PARTITIONS": "1",
        "KAFKA_TOPIC": "mouse_events",
        "LOG_LEVEL": "info",
    }
    return {
        k.lower(): os.getenv(k, default) for k, default in keys_and_defaults.items()
    }
