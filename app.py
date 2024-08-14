from http import HTTPStatus

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello() -> tuple[str, HTTPStatus]:
    return "Hello World", HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
