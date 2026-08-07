import os
from flask import Flask
from infrastructure.blueprints.welcome_controller import welcome_controller
from infrastructure.blueprints.meal_controller import meals
from infrastructure.blueprints.pwa_controller import pwa_controller

CERT_DIR = os.environ.get("CERT_DIR", "/certs")
CERT_FILE = os.path.join(CERT_DIR, 'acer-host.local.pem')
KEY_FILE = os.path.join(CERT_DIR, 'acer-host.local-key.pem')

if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "meal-tracker-dev-key-change-me")

    app.register_blueprint(welcome_controller, url_prefix="/welcome")
    app.register_blueprint(meals, url_prefix="/meals")
    app.register_blueprint(pwa_controller)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization') # list of allowed headers
        return response

    debug_boot = os.environ.get("run_debug")

    debug_var = True if debug_boot is not None and bool(debug_boot) else False
    port_var = 15002 if debug_boot is not None and bool(debug_boot) else 5002

    ssl_context = None
    if os.path.isfile(CERT_FILE) and os.path.isfile(KEY_FILE):
        ssl_context = (CERT_FILE, KEY_FILE)

    app.run(
        debug=debug_var, 
        host="0.0.0.0", 
        port=port_var,
        ssl_context=ssl_context
    )
