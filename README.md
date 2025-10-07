# MOUSE VELOCITY TRACKER

A demo Kafka project to produce analytics on the basis of mouse movement events
sent from the browser

## Testing

To run tests in your local environment, issue

```sh
make check
```

## Running

The Gateway server can be run against a locally running Kafka broker, but
the most straightforward way of running the whole setup is with docker.

Set up a `.env` file, simply copying the `.env.example` file will do

```sh
cp .env.example .env
```

And, with Docker running, issue

```sh
docker-compose up
```

The Swagger UI will be running by default on `http://localhost:8080/docs`, the API
can also be readily called with curl

```sh
curl -X 'POST' \
  'http://localhost:8080/log_mouse_movement?x=10&y=20&client_timestamp='$(date +"%Y-%m-%dT%H:%M:%S%z") \
  -H 'accept: application/json' \
  -d ''
```

## License

MIT License

Copyright (c) 2025 Gabriel Peredo
