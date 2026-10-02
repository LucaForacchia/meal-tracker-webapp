"""Tests for the weekly view: navigation by week number and lookup by date."""
import os
import sys
from unittest.mock import patch

import pytest

# Ensure src/ is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask
from infrastructure.blueprints.meal_controller import meals
from infrastructure.integrations.backend_integration import BackendIntegration, WeekNotFound


WEEK = {
    "week_number": 387,
    "total": 1,
    "meals": [{"date": "2026-09-15", "meal_type": "Pranzo", "participants": "Entrambi",
               "meal": "Tortellata", "dessert": None, "notes": ""}],
}


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


@pytest.fixture
def integration():
    with patch('infrastructure.blueprints.meal_controller.get_backend_integration') as mock_int:
        yield mock_int.return_value


# ── Controller ──────────────────────────────────────────────────────


class TestWeekView:
    def test_last_week(self, client, integration):
        """GET /meals/week shows the last week with previous/next and the date button."""
        integration.require_weekly_meal_list.return_value = WEEK

        html = client.get('/meals/week').data.decode()

        integration.require_weekly_meal_list.assert_called_once_with(None)
        assert 'Week number 387' in html
        assert 'Tortellata' in html
        assert '?week-number=386' in html
        assert '?week-number=388' in html
        assert 'Vai a data' in html
        assert 'type="date"' in html

    def test_week_by_date(self, client, integration):
        """GET /meals/week?date= asks the backend for the week containing the date."""
        integration.require_weekly_meal_list_by_date.return_value = WEEK

        html = client.get('/meals/week?date=2026-09-15').data.decode()

        integration.require_weekly_meal_list_by_date.assert_called_once_with('2026-09-15')
        integration.require_weekly_meal_list.assert_not_called()
        assert 'Week number 387' in html
        assert 'Tortellata' in html
        # navigation continues from the found week, the chosen date stays in the picker
        assert '?week-number=386' in html
        assert 'value="2026-09-15"' in html

    def test_date_out_of_tracked_period(self, client, integration):
        """404 from the backend → its message, no previous/next, link to the last week."""
        integration.require_weekly_meal_list_by_date.side_effect = WeekNotFound("Data fuori periodo tracciato")

        resp = client.get('/meals/week?date=2000-01-01')
        html = resp.data.decode()

        assert resp.status_code == 200
        assert 'Data fuori periodo tracciato' in html
        assert 'Week number' not in html
        assert 'week-number=' not in html
        assert 'Ultima settimana' in html
        assert 'value="2000-01-01"' in html

    def test_backend_error(self, client, integration):
        """Any other backend error keeps the generic message and the navigation."""
        integration.require_weekly_meal_list.side_effect = Exception("boom")

        html = client.get('/meals/week?week-number=10').data.decode()

        assert "Il backend non è d&#39;accordo" in html
        assert '?week-number=9' in html

    def test_invalid_week_number(self, client, integration):
        """A non-integer week-number shows the error page instead of a 500."""
        resp = client.get('/meals/week?week-number=abc')

        assert resp.status_code == 200
        assert "Il backend non è d&#39;accordo" in resp.data.decode()
        integration.require_weekly_meal_list.assert_not_called()


# ── Backend integration ─────────────────────────────────────────────


class TestBackendIntegration:
    def test_by_date_sends_date_param(self):
        with patch('infrastructure.integrations.backend_integration.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = WEEK

            result = BackendIntegration({"backend_url": "http://backend"}).require_weekly_meal_list_by_date('2026-09-15')

            mock_get.assert_called_once_with("http://backend/meal/week", params={"date": "2026-09-15"})
            assert result == WEEK

    def test_by_date_404_raises_week_not_found_with_backend_message(self):
        with patch('infrastructure.integrations.backend_integration.requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.json.return_value = {"error_message": "Data fuori periodo tracciato"}

            with pytest.raises(WeekNotFound) as err:
                BackendIntegration({"backend_url": "http://backend"}).require_weekly_meal_list_by_date('2000-01-01')
            assert str(err.value) == "Data fuori periodo tracciato"

    def test_by_date_other_errors(self):
        with patch('infrastructure.integrations.backend_integration.requests.get') as mock_get:
            mock_get.return_value.status_code = 400

            with pytest.raises(Exception) as err:
                BackendIntegration({"backend_url": "http://backend"}).require_weekly_meal_list_by_date('2026-13-01')
            assert not isinstance(err.value, WeekNotFound)
