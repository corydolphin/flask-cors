import re

import pytest
from flask import Flask

from flask_cors import CORS, cross_origin


@pytest.mark.parametrize("origin", ["http://[::1]:8000", "https://[2001:db8::1]", "http://[::ffff:192.0.2.1]:8080"])
@pytest.mark.parametrize("use_decorator", [False, True])
def test_literal_ipv6_origin(origin, use_decorator):
    app = Flask(__name__)

    def index():
        return "ok"

    if use_decorator:
        index = cross_origin(origins=[origin])(index)
    else:
        CORS(app, origins=[origin])
    app.add_url_rule("/", view_func=index)
    client = app.test_client()

    for requested in (origin, origin.upper()):
        response = client.get("/", headers={"Origin": requested})
        assert response.headers["Access-Control-Allow-Origin"] == requested
    for requested in (origin + "0", "http://[::2]:8000", "http://:8000"):
        response = client.get("/", headers={"Origin": requested})
        assert "Access-Control-Allow-Origin" not in response.headers


@pytest.mark.parametrize("origin", [r"http://\[::1\]:\d+$", re.compile(r"http://\[::1\]:\d+$")])
def test_ipv6_regex_origin(origin):
    app = Flask(__name__)
    CORS(app, origins=[origin])
    app.add_url_rule("/", view_func=lambda: "ok")
    client = app.test_client()
    assert (
        client.get("/", headers={"Origin": "http://[::1]:8000"}).headers["Access-Control-Allow-Origin"]
        == "http://[::1]:8000"
    )
    assert "Access-Control-Allow-Origin" not in client.get("/", headers={"Origin": "http://[::2]:8000"}).headers


def test_literal_ipv6_origin_without_request_origin():
    app = Flask(__name__)
    CORS(app, origins=["http://[::1]:8000"])
    app.add_url_rule("/", view_func=lambda: "ok")
    assert app.test_client().get("/").headers["Access-Control-Allow-Origin"] == "http://[::1]:8000"
