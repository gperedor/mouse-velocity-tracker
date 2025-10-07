import asyncio
import datetime
import re
from unittest.mock import AsyncMock, Mock

import pytest

from mouse_velocity_tracker.gateway.api import ClickstreamAPI
from mouse_velocity_tracker.gateway.producer.producer import MouseEventKafkaProducer


@pytest.fixture
def mouse_event_kafka_producer() -> MouseEventKafkaProducer:
    mekp = Mock(MouseEventKafkaProducer)
    mekp.send_event = AsyncMock()

    return mekp


def test_event_sent(mouse_event_kafka_producer: MouseEventKafkaProducer) -> None:
    api = ClickstreamAPI(
        mouse_event_kafka_producer=mouse_event_kafka_producer, kafka_topic="test_topic"
    )

    test_timestamp = datetime.datetime(2025, 1, 1)
    asyncio.run(
        api.log_mouse_movement(
            x=10, y=20, client_timestamp=test_timestamp, client_id="abc"
        )
    )

    assert hasattr(mouse_event_kafka_producer.send_event, "assert_awaited_once")
    assert isinstance(mouse_event_kafka_producer.send_event, AsyncMock)

    mouse_event_kafka_producer.send_event.assert_awaited_once()


def test_cookie_set(mouse_event_kafka_producer: MouseEventKafkaProducer):
    api = ClickstreamAPI(
        mouse_event_kafka_producer=mouse_event_kafka_producer, kafka_topic="test_topic"
    )

    test_timestamp = datetime.datetime(2025, 1, 1)
    response = asyncio.run(
        api.log_mouse_movement(x=10, y=20, client_timestamp=test_timestamp)
    )

    expected = response.headers.get("set-cookie")

    assert expected is not None, "Client-Id not set"
    assert expected != "", "Client-Id blank"

    client_id = re.match("Client-Id=([\\w\\-]+);.*", expected)[1]  # type: ignore
    assert isinstance(client_id, str)
    response = asyncio.run(
        api.log_mouse_movement(
            x=40, y=0, client_timestamp=test_timestamp, client_id=client_id
        )
    )

    assert expected == response.headers.get("set-cookie"), "Client-Id not preserved"
