VENV := $(VENV)
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python3
CMD := poetry run

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
APP := $(ROOT_DIR)/app.py

help: # Help (make help).
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

## app rules

_open_venv: ## open $(VENV) [requires VSCode!].
	code $(VENV)

activate: ## Activates $(VENV).
	. $(VENV)/bin/activate

run: ## Flask App: $(CMD) $(APP).
	$(CMD) $(APP)


## pre-commit rules

isort:
	$(VENV)/bin/isort .

black:
	$(VENV)/bin/black .

flake8:
	$(VENV)/bin/flake8 .

styles:
	make isort flake8 black

typos:
	$(VENV)/bin/mypy .

check:
	make styles typos
