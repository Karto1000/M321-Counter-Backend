import os
import random
import time
from http import HTTPStatus

import requests
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app_port = int(os.environ.get("FLASK_RUN_PORT"))
count_history = set()
other_servers: list[int] = list(filter(lambda port: port != app_port, [5000, 5001, 5002]))
host = "http://localhost"


def ping_servers() -> set[float]:
    port = random.choice(other_servers)

    try:
        response = requests.get(
            f"{host}:{port}/history",
            timeout=1
        )
    except Exception as _:
        return set()

    return set(response.json())


def update_server_history(timestamp: float):
    for port in other_servers:
        try:
            requests.put(
                f"{host}:{port}/history",
                json={"timestamp": timestamp},
                headers={"Content-Type": "application/json"},
                timeout=0.5
            )
        except Exception as _:
            print(f"Failed to update history of {port}")
            return


@app.route("/history", methods=["GET"])
def get_history() -> tuple[list[float], HTTPStatus]:
    return list(count_history), HTTPStatus.OK


@app.route("/history", methods=["PUT"])
def update_history() -> tuple[str, HTTPStatus]:
    data: dict[str, int] = request.json
    count_history.add(data.get("timestamp"))

    return "", HTTPStatus.OK


@app.route('/increment', methods=['POST'])
def increment() -> tuple[str, HTTPStatus]:
    timestamp = time.time()
    count_history.add(timestamp)
    update_server_history(timestamp)

    return str(len(count_history)), HTTPStatus.OK


@app.route("/count", methods=['GET'])
def get() -> tuple[str, HTTPStatus]:
    return str(len(count_history)), HTTPStatus.OK


if __name__ == '__main__':
    count_history = ping_servers()
    app.run(debug=True, port=int(os.environ.get("FLASK_RUN_PORT")))
