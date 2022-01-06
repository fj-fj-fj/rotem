VENV := $(VENV)
PIP := $(VENV)/bin/pip
CMD := poetry run
PYTHON := $(VENV)/bin/python3
PYTHON_VERSION := $(PYTHON_VERSION)
CURRENT_MININAL_PYTHON_VERSION := $(MININAL_PYTHON_VERSION)

ENV_FILE := .envrc
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

APP := $(ROOT_DIR)/app.py
SERVER_APP_NAME := $(SERVER_APP_NAME)

PROJECT := $(PROJECT)
CI_CONTAINER := github-actions-pipeline


help: # Show rule and description.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

browse: ## Open root page in browser (google-chrome).
	nohup google-chrome http://127.0.0.1:5000/ >> ../logs/chrome.log &

requirements.txt: ## pip freeze > requirements.txt
	poetry export --format requirements.txt --output $@ --without-hashes

activate: ## Activates $(VENV).
	. $(VENV)/bin/activate

shell: ## Python3 >>>.
	$(CMD) python3


##  ================  app  ================

run: ## Flask App: $(CMD) $(APP).
	$(CMD) $(APP)


##  ================  Check  ================

isort:
	$(VENV)/bin/isort .

black: ## Check styles with black.
	$(VENV)/bin/black .

flake8: ## Check styles with flake8.
	$(VENV)/bin/$@ . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics

styles: ## Check styles with flake8 and black.
	make flake8 black

typos: ## Check types with mypy.
	$(VENV)/bin/mypy .

check: ## Check styles and types.
	make styles typos

# https://github.com/netromdk/vermin
vermin: ## Check minimum required Pytho versions.
	@../../../.VENV_COMMON/bin/$@ -q . | head -1 | awk -F": " '{ print $$2 }'


##  ================ Commit/Push  ================

# cntl+c to break at any monent.
push: check ## Pre-push hook with "interprocess communication" (make git m="message").
	@echo "Current minimal Python version: \e[1;33m$(CURRENT_MININAL_PYTHON_VERSION)\e[0m"
	@echo "Actual Python version: \e[1;33m$$(make vermin)\e[0m"
	@python3 -c "import os; os.system('git diff' if input('git diff [Y/n]: ') in 'Yy' else '')"
	@git add -p . && git status
	@python3 -c "import os; os.system(input())"
	@git commit -m "$m" && git log -1
	@python3 -c "import os; os.system('git reset --soft HEAD~1' if input('Undo last commit [Y/n]: ') in 'Yy' else '')"
	@python3 -c "import os; os.system('git push -u origin main' if input('git push [Y/n]: ') in 'Yy' else '')"
	@python3 -c "import os; os.system('git push heroku' if input ('git push heroku [Y/n]: ') in 'Yy' else '')"

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
rpush: ## Remote: set config vars.
	heroku config:push --file $(ENV_FILE) --app $(SERVER_APP_NAME)


##  ================  Docker  ================

dserve: ## Docker: start if not starting.
	sudo service docker status > /dev/null || sudo service docker start

dstop: ## Docker: stop all containers
	docker stop $$(docker ps -aq)

drm: ## Docker: delete all containers.
	docker rm -f $$(docker ps -aq)

drmi: ## Docker: delete all images.
	docker rmi -f $$(docker images -q)

drmnone: ## Docker: remove all dangling images (tagged as <none>).
	docker rmi $$(docker images -qf dangling=true)

dclean: ## Docker: delete all containers and images.
	make drm drmi


##  ================  CI  ================

# https://github.com/nektos/act#overview----
act: # CI: run actions locally.
	./bin/act

cibuild: ## CI: build the container.
	docker build \
	--tag $(CI_CONTAINER) \
	--file .github/Dockerfile .

cirun: ## CI: run the container.
	docker run \
		-d --rm \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume $(PROJECT):/project \
		--volume $(pwd)/.github/ci-logs:/logs \
		--volume /home/vdim/.pyenv/versions/$(PYTHON_VERSION)/:/opt/hostedtoolcache/Python/$(PYTHON_VERSION)/x64/ \
		--name "$(CI_CONTAINER)" $(CI_CONTAINER)

watch-logs: ## CI: watch the logs as the pipeline progresses.
	docker exec -it $(CI_CONTAINER) /bin/sh -c "tail -f /logs/run.log"

ci: cibuild cirun ## CI: build and run the container.
	make watch-logs

cicli: ## CI: execute an interactive shell on the container.
	docker exec -it $(CI_CONTAINER) /bin/sh


##  ================  Configuration  ================

.DEFAULT: help
MAKEFLAGS += --no-print-directory
