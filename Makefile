.PHONY: clean install install-deps

clean:
	rm -rf dist/

install: install-deps
	python3 -m poetry build

install-deps:
	python3 -m pip install -r requirements.txt -r requirements-test.txt
