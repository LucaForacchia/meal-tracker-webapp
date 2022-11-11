import os
from flask import Flask
from infrastructure.blueprints.welcome_controller import welcome_controller
from infrastructure.blueprints.meal_controller import meals
from infrastructure.blueprints.replacement_controller import replacement

app = Flask(__name__)

app.register_blueprint(welcome_controller, url_prefix="/welcome")
app.register_blueprint(meals, url_prefix="/meals")
app.register_blueprint(replacement, url_prefix="/replacement")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization') # list of allowed headers
    return response

debug_boot = os.environ.get("run_debug")

if debug_boot is not None and bool(debug_boot):
    app.run(debug=True, host="0.0.0.0", port=5012)
else:
    app.run(debug=False, host="0.0.0.0", port=5002)