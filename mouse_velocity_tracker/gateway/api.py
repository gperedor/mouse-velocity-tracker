import datetime
import logging
import uuid
from typing import Annotated

from fastapi import Cookie, Response, status

import mouse_velocity_tracker.logging
from mouse_velocity_tracker.gateway.models import FrontendMouseEvent
from mouse_velocity_tracker.gateway.producer.producer import MouseEventKafkaProducer

logger: logging.Logger = mouse_velocity_tracker.logging.getLogger(__name__)


class ClickstreamAPI:
    kafka_topic: str
    mouse_event_kafka_producer: MouseEventKafkaProducer

    def __init__(
        self, mouse_event_kafka_producer: MouseEventKafkaProducer, kafka_topic: str
    ) -> None:
        self.mouse_event_kafka_producer = mouse_event_kafka_producer
        self.kafka_topic = kafka_topic

    async def log_mouse_movement(
        self,
        x: int,
        y: int,
        client_timestamp: datetime.datetime,
        client_id: Annotated[str | None, Cookie(alias="Client-Id")] = None,
    ) -> Response:
        """
        Logs an event tied to a user identified by cookie "Client-Id", generates
        id if not present in request
        """

        if client_id is None or client_id == "":
            client_id = str(uuid.uuid4())

        frontend_mouse_event = FrontendMouseEvent(
            client_id=client_id, x=x, y=y, client_timestamp=client_timestamp
        )
        logger.info(f"Received event from Client-Id: {client_id}")

        await self.mouse_event_kafka_producer.send_event(
            frontend_mouse_event=frontend_mouse_event, topic=self.kafka_topic
        )

        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.set_cookie(key="Client-Id", value=client_id, max_age=24 * 3600)

        return response
