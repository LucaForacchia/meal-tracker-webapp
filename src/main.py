import os
from flask import Flask
from infrastructure.blueprints.welcome_controller import welcome_controller
from infrastructure.blueprints.meal_controller import meals

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "meal-tracker-dev-key-change-me")

app.register_blueprint(welcome_controller, url_prefix="/welcome")
app.register_blueprint(meals, url_prefix="/meals")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization') # list of allowed headers
    return response

debug_boot = os.environ.get("run_debug")

if debug_boot is not None and bool(debug_boot):
    app.run(debug=True, host="0.0.0.0", port=15002)
else:
    app.run(debug=False, host="0.0.0.0", port=5002)