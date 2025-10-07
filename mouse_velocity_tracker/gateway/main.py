from fastapi import FastAPI

from mouse_velocity_tracker import conf
from mouse_velocity_tracker.gateway.api import ClickstreamAPI
from mouse_velocity_tracker.gateway.producer.producer import MouseEventKafkaProducer

config = conf.read_config()

kafka_producer = MouseEventKafkaProducer(
    kafka_host=config["kafka_host"], kafka_port=int(config["kafka_port"])
)
api = ClickstreamAPI(
    mouse_event_kafka_producer=kafka_producer, kafka_topic=config["kafka_topic"]
)


async def lifespan(app: FastAPI):
    await kafka_producer.startup()
    yield
    await kafka_producer.shutdown()


app = FastAPI(lifespan=lifespan)  # pyright: ignore[reportArgumentType]

app.add_api_route("/log_mouse_movement", api.log_mouse_movement, methods=["POST"])
