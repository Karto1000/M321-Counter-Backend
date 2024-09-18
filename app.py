import os
import random
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
from flask_cors import CORS

load_dotenv(find_dotenv())


def create_app() -> Flask:
    _app = Flask(__name__)
    CORS(_app)

    from routes import bp
    _app.register_blueprint(bp)

    return _app


app = create_app()
app_port = int(os.environ.get("FLASK_RUN_PORT"))
host = os.environ.get("FLASK_RUN_HOST")

if __name__ == '__main__':
    from routes import ping_servers
    
    count_history = ping_servers()
    app.run(debug=True, port=app_port, host=host)
