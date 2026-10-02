# MealTracker Webapp

version 1.0.0

Server-side rendered web frontend (Flask + Jinja + Bootstrap) of MealTracker. It lets you insert, list and delete meals, see the weekly view and the meal frequencies, talking to the _meal-tracker-backend_ REST API. It is installable on a phone home screen as a PWA.

# How to use

## Environment

The project runs on a single locked environment, identical in every context:

- **Python 3.13.12** everywhere:
  - Docker image: `python:3.13.12-slim` (see _Dockerfile_)
  - Local development and tests: `.venv` created from Python 3.13.12 (_.python-version_ pins the interpreter for pyenv)
- **Dependencies**: fully pinned. _requirements.txt_ holds the runtime ones (Flask, requests and their dependencies), installed in the Docker image; _requirements-dev.txt_ adds the test tools (pytest) for local use.

## Setup

    > python -m venv .venv                # uses Python 3.13.12 (see .python-version)
    > .venv/bin/pip install -r requirements-dev.txt

## Configuration

Driven by env variables:

| Variable | Meaning | Default |
|----------|---------|---------|
| backend_url | Base url of the backend | http://0.0.0.0:5001 |
| SECRET_KEY | Flask secret key (needed for flash messages) | development key (set a real one when deploying) |
| CERT_DIR | Folder with the HTTPS certificate and key | /certs |
| run_debug | If set, runs in debug mode on port 15002 (instead of 5002) | not set |

HTTPS is enabled only if the certificate files are found in `CERT_DIR`; otherwise the app runs on plain HTTP.

## Run the tests

    > .venv/bin/python -m pytest tests/ -v

## Local debug

    > bash run-for-testing.sh

It starts a test backend with docker-compose (_deployment/docker-compose.yml_) and runs the webapp in debug mode on port 15002.

`deployment/` is a **test-only** environment (manual and acceptance tests) that recreates the backend as if it were in a test setting, so that a new webapp version can be tried against a backend returning data. It is not used in production, which lives in the separate _meal-tracker-deployment_ folder. The backend image tag in the compose file is pinned: adjust it to the version you want to test against.

## Docker image

Build the image with the version tag:

    > bash script-docker-build.sh

## PWA

The app exposes `/manifest.json` and `/sw.js`. The service worker caches static assets (cache-first) and falls back to the last visited page on navigation errors (network-first); backend data is always online-only.
