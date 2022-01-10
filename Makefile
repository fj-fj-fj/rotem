VENV := $(VENV)
PIP := $(VENV)/bin/pip
CMD := poetry run
PYTHON := $(VENV)/bin/python3
PYTHON_VERSION := $(PYTHON_VERSION)
CURRENT_MININAL_PYTHON_VERSION := $(PYTHON_MINIMAL_VERSION)

ENV_FILE := .envrc
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

APP := $(ROOT_DIR)/app.py
SERVER_APP_NAME := $(SERVER_APP_NAME)

PROJECT := $(PROJECT)
CI_CONTAINER := github-actions-pipeline


.PHONY: help
help: # Show rule and description.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: browse
browse: ## Open root page in browser (google-chrome).
	nohup google-chrome http://127.0.0.1:5000/ >> ../logs/chrome.log &

requirements.txt: ## pip freeze > requirements.txt
	poetry export --format requirements.txt --output $@ --without-hashes

# if u switch newer python and fail
.PHONY: poetry-reinstall
poetry-reinstall: ## Poetry uninstall and install.
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_UNINSTALL=1 python &&\
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - --version 1.0.11

.PHONY: poetry-add-vendor
poetry-add-vendor: ## Add new Python version in _vendor (if make poetry-reinstall not work).
	cd -R /home/<YOU>/.poetry/lib/poetry/_vendor/py3.9 /home/<YOU>/.poetry/lib/poetry/_vendor/py3.<MINOR_NUMBER>
	find /home/<YOU>/.poetry/lib/poetry/_vendor/py3.<MINOR_NUMBER>/ -name '__pycache__' -exec rm -rf {} +
	rm poetry.lock && poetry env use $$(pyenv which python) && poetry lock && poetry install

# filter out the noise and be able to ask "which of the stuff that I installed directly
# (read: listed in pyproject.toml) has new versions available?
.PHONY: poetry-outdated
poetry-outdated: $(eval SHELL:=/bin/bash) ## Filter this to top-level dependencies only.
	poetry show --outdated | grep --file=<(poetry show --tree | grep '^\w' | cut -d' ' -f1)

##  ================  app  ================

.PHONY: run
run: ## Flask App: $(CMD) $(APP).
	$(CMD) $(APP)


##  ================  Check  ================

isort:
	$(VENV)/bin/$@ .

black: ## Check styles with black.
	$(VENV)/bin/$@ .

flake8: ## Check styles with flake8.
	$(VENV)/bin/$@ . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics \
	--exclude .git,.direnv,mypy_cashe,.pytest_cache,__pycache__,bin/,tests

.PHONY: styles
styles: ## Check styles with flake8 and black.
	make flake8 black

mypy: ## Check types with mypy.
	$(VENV)/bin/$@ .

.PHONY: check
check: ## Check styles and types.
	make styles mypy

# https://github.com/netromdk/vermin
vermin: ## Check minimal required Python versions.
	@../../../.VENV_COMMON/bin/$@ -q . | head -1 | awk -F": " '{ print $$2 }'


##  ================ Testing  ================

pytest: ## Test app with pytest.
	$(VENV)/bin/$@ .


##  ================ Commit/Push  ================

# cntl+c to break at any monent.
.PHONY: push
push: check pytest ## Pre-push hook with "interprocess communication" (make git m="message").
	@poetry show --outdated
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
.PHONY: rpush
rpush: ## Remote: set config vars.
	heroku config:push --file $(ENV_FILE) --app $(SERVER_APP_NAME)


##  ================  Docker  ================

.PHONY: dserve
dserve: ## Docker: start if not starting.
	sudo service docker status > /dev/null || sudo service docker start

.PHONY: dstop
dstop: ## Docker: stop all containers
	docker stop $$(docker ps -aq)

.PHONY: drm
drm: ## Docker: delete all containers.
	docker rm -f $$(docker ps -aq)

.PHONY: drmi
drmi: ## Docker: delete all images.
	docker rmi -f $$(docker images -q)

.PHONY: drmnone
drmnone: ## Docker: remove all dangling images (tagged as <none>).
	docker rmi $$(docker images -qf dangling=true)

.PHONY: dclean
dclean: ## Docker: delete all containers and images.
	make drm drmi


##  ================  CI  ================

# https://github.com/nektos/act#overview----
act: # CI: run actions locally.
	./bin/$@

.PHONY: cibuild
cibuild: ## CI: build the container.
	docker build \
	--tag $(CI_CONTAINER) \
	--file .github/Dockerfile .

.PHONY: cirun
cirun: ## CI: run the container.
	docker run \
		-d --rm \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume $(PROJECT):/project \
		--volume $(pwd)/.github/ci-logs:/logs \
		--volume /home/vdim/.pyenv/versions/$(PYTHON_VERSION)/:/opt/hostedtoolcache/Python/$(PYTHON_VERSION)/x64/ \
		--name "$(CI_CONTAINER)" $(CI_CONTAINER)

.PHONY: watch-logs
watch-logs: ## CI: watch the logs as the pipeline progresses.
	docker exec -it $(CI_CONTAINER) /bin/sh -c "tail -f /logs/run.log"

.PHONY: ci
ci: cibuild cirun ## CI: build and run the container.
	make watch-logs

.PHONY: cicli
cicli: ## CI: execute an interactive shell on the container.
	docker exec -it $(CI_CONTAINER) /bin/sh


##  ================  Configuration  ================

.DEFAULT: help
MAKEFLAGS += --no-print-directory
