"""Tests for the meal insertion form and controller."""
import sys
import os
from datetime import date
from unittest.mock import patch, MagicMock

import pytest

# Ensure src/ is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, get_flashed_messages
from infrastructure.blueprints.meal_controller import meals


@pytest.fixture
def app():
    """Create a test Flask app with the meals blueprint."""
    tmpl = os.path.join(os.path.dirname(__file__), '..', 'src', 'templates')
    app = Flask(__name__, template_folder=tmpl)
    app.secret_key = 'test-secret'
    app.register_blueprint(meals, url_prefix='/meals')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# ── GET ──────────────────────────────────────────────────────────────


class TestGetForm:
    def test_renders_with_today_date(self, client):
        """GET /meals/ returns 200 with today's date in the value attr."""
        with patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_integration:
            mock_integration.return_value.require_meals_list.return_value = ['Pizza', 'Pasta']

            resp = client.get('/meals/')
            assert resp.status_code == 200
            html = resp.data.decode()
            today = date.today().isoformat()
            assert f'value="{today}"' in html

    def test_renders_form_structure(self, client):
        """GET /meals/ contains the compact form elements."""
        with patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_integration:
            mock_integration.return_value.require_meals_list.return_value = []

            resp = client.get('/meals/')
            html = resp.data.decode()
            assert 'Nuovo pasto' in html
            assert 'form-control-lg' in html
            assert 'Salva pasto' in html
            assert 'custom-switch' in html
            assert 'toggleStartWeek' in html

    def test_renders_row_layout(self, client):
        """GET /meals/ has side-by-side rows (col-6)."""
        with patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_integration:
            mock_integration.return_value.require_meals_list.return_value = []

            resp = client.get('/meals/')
            html = resp.data.decode()
            # 2 col-6 pairs: Chi+Tipo, Dessert+Note
            assert html.count('col-6') == 4

    def test_meal_field_not_required(self, client):
        """The meal text field must not be required (an empty meal is allowed)."""
        with patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_integration:
            mock_integration.return_value.require_meals_list.return_value = []

            resp = client.get('/meals/')
            html = resp.data.decode()
            assert 'id="meal"' in html
            assert 'required' not in html


# ── POST: start_week ─────────────────────────────────────────────────


class TestStartWeek:
    def test_without_start_week_sends_false(self, client):
        """POST without toggling Start week → start_week: False."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post:
            mock_post.return_value.status_code = 201

            resp = client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'notes': '',
            })

            assert resp.status_code == 302
            call_args = mock_post.call_args
            sent_payload = call_args[1]['json']
            assert sent_payload['start_week'] is False

    def test_with_start_week_sends_true(self, client):
        """POST with Start week=on → start_week: True."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post:
            mock_post.return_value.status_code = 201

            resp = client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'Start week': 'on',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'notes': '',
            })

            assert resp.status_code == 302
            call_args = mock_post.call_args
            sent_payload = call_args[1]['json']
            assert sent_payload['start_week'] is True

    def test_start_week_empty_value_sends_false(self, client):
        """POST with Start week='' (not toggled, but hidden input present) → start_week: False."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post:
            mock_post.return_value.status_code = 201

            resp = client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'Start week': '',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'notes': '',
            })

            assert resp.status_code == 302
            call_args = mock_post.call_args
            sent_payload = call_args[1]['json']
            assert sent_payload['start_week'] is False


# ── POST: dessert ────────────────────────────────────────────────────


class TestDessert:
    def test_with_dessert_sends_dessert_field(self, client):
        """POST with dessert filled → dessert key in payload."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post:
            mock_post.return_value.status_code = 201

            client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'dessert': 'Tiramisù',
                'notes': '',
            }, follow_redirects=True)

            call_args = mock_post.call_args
            sent_payload = call_args[1]['json']
            assert 'dessert' in sent_payload
            assert sent_payload['dessert'] == 'Tiramisù'

    def test_without_dessert_omits_field(self, client):
        """POST without dessert → dessert not in payload."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post:
            mock_post.return_value.status_code = 201

            client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'notes': '',
            }, follow_redirects=True)

            call_args = mock_post.call_args
            sent_payload = call_args[1]['json']
            assert 'dessert' not in sent_payload

    def test_empty_dessert_omits_field(self, client):
        """POST with dessert='' → dessert not in payload."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post:
            mock_post.return_value.status_code = 201

            client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'dessert': '',
                'notes': '',
            }, follow_redirects=True)

            call_args = mock_post.call_args
            sent_payload = call_args[1]['json']
            assert 'dessert' not in sent_payload


# ── POST: flash messages ─────────────────────────────────────────────


class TestFlashMessages:
    def test_success_flashes_and_redirects(self, client):
        """201 from backend → redirect 302, then success flash on final page."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post, \
             patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_int:
            mock_post.return_value.status_code = 201
            mock_int.return_value.require_meals_list.return_value = []

            resp = client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'notes': '',
            }, follow_redirects=True)

            assert resp.status_code == 200
            html = resp.data.decode()
            assert 'Pasto inserito' in html

    def test_failure_flashes_error(self, client):
        """500 from backend → redirect 302, then error flash on final page."""
        with patch('infrastructure.blueprints.meal_controller.requests.post') as mock_post, \
             patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_int:
            mock_post.return_value.status_code = 500
            mock_int.return_value.require_meals_list.return_value = []

            resp = client.post('/meals/', data={
                'dateMeal': '2026-08-03',
                'meal_type': 'Pranzo',
                'participants': 'Entrambi',
                'meal': 'Tortellata',
                'notes': '',
            }, follow_redirects=True)

            assert resp.status_code == 200
            html = resp.data.decode()
            assert 'Errore durante' in html
