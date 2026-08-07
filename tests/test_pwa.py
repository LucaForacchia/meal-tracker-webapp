"""Tests for PWA support: manifest, service worker and base template hooks."""
import json
import os
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


# ── Manifest ────────────────────────────────────────────────────────


class TestManifest:
    def test_served_as_json(self, client):
        """GET /manifest.json returns a valid web app manifest."""
        resp = client.get('/manifest.json')
        assert resp.status_code == 200
        assert resp.content_type.startswith('application/json')
        manifest = json.loads(resp.data)
        assert manifest['name'] == 'MealTracker'
        assert manifest['short_name'] == 'Meals'
        assert manifest['start_url'] == '/welcome'
        assert manifest['scope'] == '/'
        assert manifest['display'] == 'standalone'

    def test_icons_declared_and_present(self, client):
        """Manifest declares 192 and 512 icons and the files are served."""
        resp = client.get('/manifest.json')
        manifest = json.loads(resp.data)
        sizes = {icon['sizes'] for icon in manifest['icons']}
        assert '192x192' in sizes
        assert '512x512' in sizes
        for icon in manifest['icons']:
            assert client.get(icon['src']).status_code == 200, icon['src']


# ── Service worker ──────────────────────────────────────────────────


class TestServiceWorker:
    def test_served_at_root_scope(self, client):
        """GET /sw.js returns JS containing the cache strategy."""
        resp = client.get('/sw.js')
        assert resp.status_code == 200
        assert 'text/javascript' in resp.content_type
        assert b'PRECACHE_URLS' in resp.data
        assert b'networkFirst' in resp.data


# ── base.html hooks ─────────────────────────────────────────────────


class TestBaseTemplate:
    def test_pwa_hooks_present(self, app, client):
        """base.html links the manifest and registers the service worker."""
        with app.test_request_context():
            html = render_template('base.html')
        assert 'rel="manifest" href="/manifest.json"' in html
        assert 'name="theme-color" content="#343a40"' in html
        assert 'apple-touch-icon' in html
        assert 'navigator.serviceWorker' in html
        assert "register('/sw.js')" in html
