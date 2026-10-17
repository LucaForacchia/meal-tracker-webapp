"""Tests for PWA support: manifest, service worker and base template hooks."""
import json
import os
import re
import struct
import sys

import pytest

# Ensure src/ is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, render_template
from infrastructure.blueprints.pwa_controller import pwa_controller


@pytest.fixture
def app():
    """Create a test Flask app with the PWA blueprint."""
    base = os.path.join(os.path.dirname(__file__), '..', 'src')
    app = Flask(__name__, template_folder=os.path.join(base, 'templates'),
                static_folder=os.path.join(base, 'static'))
    app.register_blueprint(pwa_controller)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# Requests from the two origins the app is installed from
HOME = {'Host': 'acer-host.local:5002'}
TAILSCALE = {'Host': 'laptop-home.tail1234.ts.net'}
TAILSCALE_PROXIED = {'Host': '127.0.0.1:5002', 'X-Forwarded-Host': 'laptop-home.tail1234.ts.net'}


def png_size(data):
    """(width, height) read from the PNG header."""
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    return struct.unpack('>II', data[16:24])


# ── Manifest ────────────────────────────────────────────────────────


class TestManifest:
    def test_served_as_manifest(self, client):
        """GET /manifest.json returns a valid web app manifest."""
        resp = client.get('/manifest.json', headers=HOME)
        assert resp.status_code == 200
        assert resp.content_type == 'application/manifest+json'
        manifest = json.loads(resp.data)
        assert manifest['start_url'] == '/welcome'
        assert manifest['scope'] == '/'
        assert manifest['display'] == 'standalone'

    def test_home_variant(self, client):
        """Home network: MealTracker, blue, icon-* icons."""
        manifest = json.loads(client.get('/manifest.json', headers=HOME).data)
        assert manifest['name'] == 'MealTracker'
        assert manifest['short_name'] == 'Meals'
        assert manifest['theme_color'] == '#1e5fa8'
        assert manifest['background_color'] == '#1e5fa8'
        assert [icon['src'] for icon in manifest['icons']] == [
            '/static/icons/icon-192.png',
            '/static/icons/icon-512.png',
            '/static/icons/icon-maskable-512.png',
        ]

    @pytest.mark.parametrize('headers', [TAILSCALE, TAILSCALE_PROXIED],
                             ids=['host', 'x-forwarded-host'])
    def test_tailscale_variant(self, client, headers):
        """Tailscale (*.ts.net, as Host or forwarded host): VPN Meals, green, vpn-icon-* icons."""
        manifest = json.loads(client.get('/manifest.json', headers=headers).data)
        assert manifest['name'] == 'VPN Meals'
        assert manifest['short_name'] == 'VPN Meals'
        assert manifest['theme_color'] == '#2e8b57'
        assert manifest['background_color'] == '#2e8b57'
        assert [icon['src'] for icon in manifest['icons']] == [
            '/static/icons/vpn-icon-192.png',
            '/static/icons/vpn-icon-512.png',
            '/static/icons/vpn-icon-maskable-512.png',
        ]

    @pytest.mark.parametrize('headers', [HOME, TAILSCALE], ids=['home', 'tailscale'])
    def test_icons_present_with_declared_size(self, client, headers):
        """Every declared icon is served, opaque, with the size the manifest declares."""
        manifest = json.loads(client.get('/manifest.json', headers=headers).data)
        assert {icon['purpose'] for icon in manifest['icons']} == {'any', 'maskable'}
        for icon in manifest['icons']:
            resp = client.get(icon['src'])
            assert resp.status_code == 200, icon['src']
            width, height = png_size(resp.data)
            assert icon['sizes'] == f'{width}x{height}', icon['src']
            assert resp.data[25] == 2, f"{icon['src']} is not RGB (opaque)"


# ── Service worker ──────────────────────────────────────────────────


class TestServiceWorker:
    def test_served_at_root_scope(self, client):
        """GET /sw.js returns JS containing the cache strategy."""
        resp = client.get('/sw.js')
        assert resp.status_code == 200
        assert 'text/javascript' in resp.content_type
        assert b'PRECACHE_URLS' in resp.data
        assert b'networkFirst' in resp.data

    def test_cache_name_bumped(self, client):
        """Cache v3 drops the old icons, cached cache-first at the same URLs (1.2.0)."""
        assert b"CACHE_NAME = 'mealtracker-v3'" in client.get('/sw.js').data


# ── Server reachability ─────────────────────────────────────────────


class TestPing:
    def test_ping(self, client):
        """GET /ping answers 204 with no body."""
        resp = client.get('/ping')
        assert resp.status_code == 204
        assert resp.data == b''


# ── base.html hooks ─────────────────────────────────────────────────


class TestBaseTemplate:
    def test_pwa_hooks_present(self, app, client):
        """base.html links the manifest and registers the service worker."""
        with app.test_request_context(headers=HOME):
            html = render_template('base.html')
        assert 'rel="manifest" href="/manifest.json"' in html
        assert 'name="theme-color" content="#1e5fa8"' in html
        assert 'rel="apple-touch-icon" href="/static/icons/icon-192.png"' in html
        assert 'name="apple-mobile-web-app-title" content="MealTracker"' in html
        assert 'navigator.serviceWorker' in html
        assert "register('/sw.js')" in html

    def test_tailscale_variant(self, app, client):
        """Behind Tailscale base.html shows the VPN color, icon and title."""
        with app.test_request_context(headers=TAILSCALE):
            html = render_template('base.html')
        assert 'name="theme-color" content="#2e8b57"' in html
        assert 'rel="apple-touch-icon" href="/static/icons/vpn-icon-192.png"' in html
        assert 'name="apple-mobile-web-app-title" content="VPN Meals"' in html

    def test_stale_copy_banner(self, app, client):
        """base.html carries its render time and the banner shown when /ping fails."""
        with app.test_request_context():
            html = render_template('base.html')
        assert re.search(r'<body data-rendered-at="\d{13}">', html)
        assert 'id="staleCopyBanner"' in html
        assert "fetch('/ping'" in html
        assert 'Non connesso al server.' in html
        assert 'Copia del ' in html
