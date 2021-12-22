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
	make flake8 black

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

# cntl+c to break at any monent.
push: check ## Pre-push hook with "interprocess communication" (make git m="message").
	@python3 -c "import os; os.system('git diff' if input('git diff [Y/n]: ') in 'Yy' else '')"
	git add . && git status
	@python3 -c "import os; os.system(input())"
	git commit -m "$m" && git log -1
	@python3 -c "import os; os.system('git reset --soft HEAD~1' if input('Undo last commit [Y/n]: ') in 'Yy' else '')"
	@python3 -c "import os; os.system('git push -u origin main' if input('git push [Y/n]: ') in 'Yy' else '')"
	@python3 -c "import os; os.system('git push $(SERVER)' if input ('git push $(SERVER) [Y/n]: ') in 'Yy' else '')"
