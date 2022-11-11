import os
from flask import Blueprint, render_template, url_for, current_app
from infrastructure.config import get_current_version

welcome_controller = Blueprint("welcome", __name__, template_folder="templates", static_folder="static", static_url_path='../static')

@welcome_controller.route("/")
def home():
    return render_template("home_page.html", version = get_current_version())