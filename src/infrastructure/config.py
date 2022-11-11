import os
from flask import g

from .integrations.backend_integration import BackendIntegration

def get_current_version():
    return "0.0.2"

def load_config():
    config = {}

    config["backend_url"] = os.environ.get("backend_url")
    if config["backend_url"] is None:
        config["backend_url"] = "http://0.0.0.0:5001"

    return config

def get_config():
    config = getattr(g, "_config", None)

    if config is None:
        config = load_config()
        g._config = config

    return config
    
def get_backend_integration():
    integration = getattr(g, "_backend_integration", None)

    if integration is None:

        config = load_config()

        integration = BackendIntegration(config)
        
        g._backend_integration = integration

    return integration