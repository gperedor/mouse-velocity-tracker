.PHONY: check clean fmt install install-deps lint
SOURCE_DIRS := mouse_velocity_tracker test

check: install-deps
	python3 -m pytest test

clean:
	rm -rf dist/

fmt:
	black $(SOURCE_DIRS)
	isort $(SOURCE_DIRS)

install: install-deps
	python3 -m poetry build

install-deps:
	python3 -m pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt

lint:
	black --check ${SOURCE_DIRS}
	isort --check ${SOURCE_DIRS}
	flake8 ${SOURCE_DIRS}
