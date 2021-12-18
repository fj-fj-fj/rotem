VENV := $(VENV)
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python3
CMD := poetry run

ENV_FILE := .envrc
SERVER := $(SERVER)
SERVER_APP_NAME := $(SERVER_APP_NAME)

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

# https://devcenter.heroku.com/articles/heroku-cli
# install heroku-cli:
#   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
#   heroku --version
#   heroku login or heroku login -i
#   heroku git:remote -a $(SERVER_APP_NAME)
# Poetry build pack for Heroku:
#   heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git -a $(SERVER_APP_NAME)
#   heroku buildpacks:clear -a $(SERVER_APP_NAME)
#   heroku buildpacks:add heroku/python -a $(SERVER_APP_NAME)
# https://devcenter.heroku.com/articles/config-vars
# https://github.com/xavdid/heroku-config:
#   heroku plugins:install heroku-config

remote-env: ## Remote: set config vars.
	heroku config:push --file $(ENV_FILE) --app $(SERVER_APP_NAME)
