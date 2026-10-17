"""PWA routes: web app manifest and service worker.

Both files live in the app static folder, but are served from the root path:
the service worker MUST be served from a URL whose scope covers the whole app
(from /static/ its scope would be limited to /static/).

The app is reached from two origins, each installed as its own PWA: the home network
(variant "casa", static manifest.json as is) and Tailscale (hosts *.ts.net, variant
"vpn"). The manifest and the base.html meta tags change with the variant, so that the
two installed apps have a different name, color and icon.
"""
import json
import os
import time

from flask import Blueprint, current_app, request

pwa_controller = Blueprint("pwa", __name__)


PWA_VARIANTS = {
    "casa": {
        "name": "MealTracker",
        "short_name": "Meals",
        "theme_color": "#1e5fa8",
        "theme_color_dark": "#184c86",
        "icon_prefix": "icon-",
    },
    "vpn": {
        "name": "VPN Meals",
        "short_name": "VPN Meals",
        "theme_color": "#2e8b57",
        "theme_color_dark": "#256f46",
        "icon_prefix": "vpn-icon-",
    },
}


def pwa_variant():
    """Variant of the current request: "vpn" behind Tailscale (*.ts.net), "casa" otherwise.

    The host forwarded by a reverse proxy (X-Forwarded-Host) wins over the Host header.
    """
    host = request.headers.get("X-Forwarded-Host") or request.host or ""
    host = host.split(",")[0].strip().split(":")[0].lower()
    return PWA_VARIANTS["vpn" if host.endswith(".ts.net") else "casa"]


@pwa_controller.app_context_processor
def pwa_template_values():
    """Values used by base.html on every page.

    rendered_at: render time (epoch ms, formatted by the browser in its own timezone).
    When the server is not reachable the service worker serves the last cached copy of a
    page: base.html then shows "Non connesso al server. Copia del <rendered_at>".
    pwa: variant (name, colors, icons) of the origin the page is served from; its
    colors are also the palette of the page (navbar, buttons, switches, links).
    """
    return {"rendered_at": int(time.time() * 1000), "pwa": pwa_variant()}


@pwa_controller.route("/ping")
def ping():
    """Reachability check used by base.html (never cached by the service worker)."""
    return "", 204


@pwa_controller.route("/manifest.json")
def manifest():
    """Static manifest.json, with name, colors and icons of the request variant."""
    with open(os.path.join(current_app.static_folder, "manifest.json")) as manifest_file:
        manifest = json.load(manifest_file)

    variant = pwa_variant()
    manifest["name"] = variant["name"]
    manifest["short_name"] = variant["short_name"]
    manifest["theme_color"] = variant["theme_color"]
    manifest["background_color"] = variant["theme_color"]
    for icon in manifest["icons"]:
        icon["src"] = icon["src"].replace("/icon-", "/" + variant["icon_prefix"])

    return current_app.response_class(
        json.dumps(manifest, ensure_ascii=False, indent=2), mimetype="application/manifest+json")


@pwa_controller.route("/sw.js")
def service_worker():
    response = current_app.send_static_file("sw.js")
    response.headers["Content-Type"] = "text/javascript"
    return response
