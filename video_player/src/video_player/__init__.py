import os
import logging

# General configuration object
from utils_config import LOG_FORMAT
# Logging level for the container
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# Modules installed from this environment
from api import app

def main():
    logging.info("Starting app")
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )