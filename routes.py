import os
import random
import time
from http import HTTPStatus

import requests
from flask import Blueprint, request

bp = Blueprint(__name__, "")

other_servers: list[str] = os.environ.get("FLASK_RUN_OTHER_SERVERS").strip().split(",")

count_history = set()


def ping_servers() -> set[float]:
    host = random.choice(other_servers)

    try:
        response = requests.get(
            f"http://{host}/history",
            timeout=1
        )
    except Exception as _:
        return set()

    return set(response.json())


def update_server_history(timestamp: float):
    for host in other_servers:
        try:
            requests.put(
                f"http://{host}/history",
                json={"timestamp": timestamp},
                headers={"Content-Type": "application/json"},
                timeout=0.5
            )
        except Exception as _:
            print(f"Failed to update history of {host}")
            return


@bp.route("/history", methods=["GET"])
def get_history() -> tuple[list[float], HTTPStatus]:
    return list(count_history), HTTPStatus.OK


@bp.route("/history", methods=["PUT"])
def update_history() -> tuple[str, HTTPStatus]:
    data: dict[str, int] = request.json
    count_history.add(data.get("timestamp"))

    return "", HTTPStatus.OK


@bp.route('/increment', methods=['POST'])
def increment() -> tuple[str, HTTPStatus]:
    timestamp = time.time()
    count_history.add(timestamp)
    update_server_history(timestamp)

    return str(len(count_history)), HTTPStatus.OK


@bp.route("/count", methods=['GET'])
def get() -> tuple[str, HTTPStatus]:
    return str(len(count_history)), HTTPStatus.OK
