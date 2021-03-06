# You can just use `make help` to read all rules.
# tl;dr: `make pytest run` to run tests and start Flask server.

# Python constants
VENV := $(VENV)
PIP := $(VENV)/bin/pip
PYTHON := $(VENV)/bin/python3
PYTHON_VERSION := $(PYTHON_VERSION)
CURRENT_MININAL_PYTHON_VERSION := $(PYTHON_MINIMAL_VERSION)

# files/dirs
ENV_FILE := .envrc
PROJECT_ROOT:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# __main__
APP := $(PROJECT_ROOT)/app.py

# Remote app name
SERVER_APP_NAME := $(SERVER_APP_NAME)

# Docker containers
APP_CONTAINER := rotem-flask-application
CI_CONTAINER := github-actions-pipeline


.PHONY: help
help: # Show rule and description.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: run
run: ## Start local server.
	poetry run $(APP)
# Clear Google Chrome Redirect Cache for a single URL
# chrome / cntl+shift+j / network / fetch('http://127.0.0.1:5000', {method: 'post'}).then(()=>{})
# * or any other wesite with a non-restrictive CORS policy.

##  ================ Requirements  ================

# https://python-poetry.org/docs/cli/

.PHONY: requirements.txt
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


##  ================  Check  ================
# isort, black, flake8, mypy, vermin, grep

.PHONY: warnings
warnings: ## Find temporary fixes, prints, forgotten notes and/or possible issues with `grep`.
	@grep --color="always" --include=\*.{py,js} --exclude-dir=".direnv" \
	-i -r -n -w $(PROJECT_ROOT) -e 'FIXME\|issue\|problem\|nosec\|print\|console.log' || test $$? = 1;

# https://pycqa.github.io/isort/docs/configuration/options.html
isort: ## Sort imports with isort.
	@$(VENV)/bin/$@ .

# https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html
black: ## Check styles with black.
	@$(VENV)/bin/$@ .

# https://flake8.pycqa.org/en/latest/user/options.html
flake8: ## Check styles with flake8.
	@$(VENV)/bin/$@ . --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics \
	--exclude .git,.direnv,mypy_cashe,.pytest_cache,__pycache__,bin/,tests

.PHONY: styles
styles: ## Check styles with flake8 and black.
	make black flake8

# https://mypy.readthedocs.io/en/stable/command_line.html
mypy: ## Check types with mypy.
	@$(VENV)/bin/$@ .

.PHONY: check
check: ## Check styles and types.
	make styles mypy

# https://github.com/netromdk/vermin
vermin: ## Check minimal required Python versions.
	@../../../.VENV_COMMON/bin/$@ -q . | head -1 | awk -F": " '{ print $$2 }'

.PHONY: diff-includefiles
diff-includefiles: ## Compare .*ignore files line by line.
	@grep -Fxvf .dockerignore .gitignore | { grep -v '!/\|.github' || test $$? = 1; }


##  ================ Security  ================
# Bandit, Safety
# https://python-security.readthedocs.io/

# https://bandit.readthedocs.io/en/latest/config.html
bandit: ## Find common security issues in Python code with Bandit.
	@$(VENV)/bin/$@ --recursive app.py ./app

# https://pypi.org/project/safety/
safety: ## Check installed dependencies for known vulnerabilities with Safety.
	@poetry export --without-hashes -f requirements.txt | $(VENV)/bin/$@ check --full-report --stdin

.PHONY: security
security: bandit safety ## Guard with Bandit and Safety.

##  ================ Test  ================
# pytest, coverage

# https://docs.pytest.org/en/latest/reference/customize.html#command-line-options-and-configuration-file-settings
pytest: ## Test app with pytest.
	@$(VENV)/bin/$@ .

# https://coverage.readthedocs.io/en/coverage-3.5.3/cmd.html
coverage: ## Measure code with coverage.
	@$(VENV)/bin/$@ run --source=. -m pytest .
	@$(VENV)/bin/$@ report -m
	@$(VENV)/bin/$@ html

.PHONY: tests
tests: ## Test with pytest, coverage and check dev artifacts.
	make coverage warnings


##  ================ Commit/Push  ================
# `git push`, `heroku config:push`

# cntl+c to break at any monent.
.PHONY: push
push: check tests ## Pre-push hook with "interprocess communication" (make git m="message").
	@poetry show --outdated
	@make requirements.txt
	@echo "Current minimal Python version: \e[1;33m$(CURRENT_MININAL_PYTHON_VERSION)\e[0m"
	@echo "Actual Python version: \e[1;33m$$(make vermin)\e[0m"
	@make warnings diff-includefiles security
	@python3 -c "import os; os.system(input())"
	@python3 -c "import os; os.system('git diff' if input('git diff [Y/n]: ') in 'Yy' else '')"
	@git add -p . && git status
	@python3 -c "import os; os.system(input())"
	@git commit -m "$m" && git log -1
	@python3 -c "import os; os.system('git reset --soft HEAD~1' if input('Undo last commit [Y/n]: ') in 'Yy' else '')"
	@python3 -c "import os; os.system('git push -u origin main' if input('git push [Y/n]: ') in 'Yy' else '')"
	@python3 -c "import os; os.system('git push heroku' if input ('git push heroku [Y/n]: ') in 'Yy' else '')"


# https://devcenter.heroku.com/articles/heroku-cli
# curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
# heroku --version
# heroku login (or heroku login -i)
# heroku git:remote -a $(SERVER_APP_NAME)
# heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git -a $(SERVER_APP_NAME)
# heroku buildpacks:clear -a $(SERVER_APP_NAME)
# heroku buildpacks:add heroku/python -a $(SERVER_APP_NAME)
# https://devcenter.heroku.com/articles/config-vars
# https://github.com/xavdid/heroku-config:
# heroku plugins:install heroku-config
.PHONY: rset
rset: ## Remote: set config vars.
	heroku config:push --file $(ENV_FILE) --app $(SERVER_APP_NAME)


##  ================  Docker  ================
# dev, ci

# https://snyk.io/advisor/docker/python/3.10
# docker pull python:3.10-slim
# docker images --digests | grep python
# [...] sha256:ca2a31f21938f24bab02344bf846a90cc2bff5bd0e5a53b24b5dfcb4519ea8a3

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


##  ----------------  docker dev  ----------------

dbuild: dserve ## Build the Dockerfile and tag the image as $(APP_CONTAINER).
	docker build --tag $(APP_CONTAINER) .

drun: dserve ## Start the container with configs.
	docker run \
	--env FLASK_SECRET_KEY \
	--env NEWSAPI_KEY \
	--env TZ=$$(cat /etc/timezone) \
	--publish 5000:5000 $(APP_CONTAINER)

# fatal error: runtime: out of memory?
# wsl --shutdown
# df -h

dup: dbuild drun ## APP: build and run.

# npm install -g snyk
dscan: ## APP: scanne containerized Python app with Snyk.
	snyk container test $(APP_CONTAINER)

dcli: ## APP: execute an interactive shell on the container.
	docker exec -it $(APP_CONTAINER) /bin/sh


##  ----------------  docker CI  ----------------

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


##  ================  make configuration  ================

.DEFAULT: help
MAKEFLAGS += --no-print-directory
