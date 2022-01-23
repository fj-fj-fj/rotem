FROM python:3.10-slim as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential gcc

WORKDIR /usr/app
RUN python3 -m venv /usr/app/.venv
ENV PATH="/usr/app/.venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim@sha256:ca2a31f21938f24bab02344bf846a90cc2bff5bd0e5a53b24b5dfcb4519ea8a3

RUN groupadd -g 999 py_flask && \
    useradd -r -u 999 -g py_flask py_flask

RUN mkdir /usr/app && chown py_flask:py_flask /usr/app
WORKDIR /usr/app/

COPY --chown=py_flask:py_flask --from=build /usr/app/.venv ./.venv
COPY --chown=py_flask:py_flask . .

USER 999

ENV PATH="/usr/app/.venv/bin:$PATH"
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]

# Ensure that your application is well monitored for health status.
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:5000/health
