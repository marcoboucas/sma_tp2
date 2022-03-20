sources = communication pw_argumentation.py runtests.py

# CODE
lint:
	python -m isort $(sources)
	python -m black $(sources)
	python -m pylint $(sources)
	python -m flake8 $(sources)
	python -m mypy $(sources)

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt


# TESTS
test-pref:
	python -m communication.preferences.Preferences


test: test-pref
	python -m runtests
