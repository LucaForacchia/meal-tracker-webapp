# MealTracker Webapp

version 1.0.0

Server-side rendered web frontend (Flask + Jinja + Bootstrap) of MealTracker. It lets you insert, list and delete meals, see the weekly view and the meal frequencies, talking to the _meal-tracker-backend_ REST API. It is installable on a phone home screen as a PWA.

# How to use

## Environment

- Python 3.10 in Docker (`python:3.10-slim`, see _Dockerfile_); dependencies in _requirements.txt_ (Flask, requests)
- Upgrading to a newer Python (at least 3.12) is tracked in _TODO.md_

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

    > pytest tests/ -v

## Local debug

    > bash run-for-testing.sh

It starts a test backend with docker-compose (_deployment/docker-compose.yml_) and runs the webapp in debug mode on port 15002.

`deployment/` is a **test-only** environment (manual and acceptance tests) that recreates the backend as if it were in a test setting, so that a new webapp version can be tried against a backend returning data. It is not used in production, which lives in the separate _meal-tracker-deployment_ folder. The backend image tag in the compose file is pinned: adjust it to the version you want to test against.

## Docker image

Build the image with the version tag:

    > bash script-docker-build.sh

## PWA

The app exposes `/manifest.json` and `/sw.js`. The service worker caches static assets (cache-first) and falls back to the last visited page on navigation errors (network-first); backend data is always online-only.
