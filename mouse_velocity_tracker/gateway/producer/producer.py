from __future__ import annotations

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError

import mouse_velocity_tracker.logging
from mouse_velocity_tracker.gateway.models import FrontendMouseEvent

logger = mouse_velocity_tracker.logging.getLogger(__name__)


class MouseEventKafkaProducer:
    """
    A service class to send events to the Kafka broker.

    The implementation is asynchronous, and batches events for sending
    """

    kafka_host: str
    kafka_port: int
    kafka_producer: AIOKafkaProducer

    def __init__(self, kafka_host: str, kafka_port: int) -> None:
        self.kafka_host = kafka_host
        self.kafka_port = kafka_port
        self.kafka_producer = AIOKafkaProducer(
            bootstrap_servers=f"{kafka_host}:{kafka_port}",
            enable_idempotence=True,
            linger_ms=50,
        )

    async def startup(self) -> None:
        logger.info(f"Connecting to Broker at {self.kafka_host}:{self.kafka_port}")
        await self.kafka_producer.start()

    async def shutdown(self) -> None:
        await self.kafka_producer.stop()

    async def send_event(
        self, topic: str, frontend_mouse_event: FrontendMouseEvent
    ) -> None:
        """
        Sends a mouse movement event to the Kafka broker
        """
        try:
            logger.info(
                "Batching event: {event}, topic: {topic}".format(
                    event=frontend_mouse_event.model_dump_json(), topic=topic
                )
            )

            await self.kafka_producer.send(
                topic=topic,
                key=frontend_mouse_event.client_id.encode(),
                value=frontend_mouse_event.model_dump_json().encode(),
            )
        except KafkaTimeoutError as e:
            logger.error(f"Kafka broker timeout: {e}")
