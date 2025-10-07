FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt requirements.txt

COPY mouse_velocity_tracker/ ./mouse_velocity_tracker

RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn mouse_velocity_tracker.gateway.main:app --log-level ${LOG_LEVEL} --reload --reload-dir /app/mouse_velocity_tracker/gateway --host 0.0.0.0 --port  ${GATEWAY_PORT}"]
