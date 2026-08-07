"""PWA routes: web app manifest and service worker.

Both files live in the app static folder, but are served from the root path:
the service worker MUST be served from a URL whose scope covers the whole app
(from /static/ its scope would be limited to /static/).
"""
from flask import Blueprint, current_app

pwa_controller = Blueprint("pwa", __name__)


@pwa_controller.route("/manifest.json")
def manifest():
    response = current_app.send_static_file("manifest.json")
    response.headers["Content-Type"] = "application/json"
    return response


@pwa_controller.route("/sw.js")
def service_worker():
    response = current_app.send_static_file("sw.js")
    response.headers["Content-Type"] = "text/javascript"
    return response
