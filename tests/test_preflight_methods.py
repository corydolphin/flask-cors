"""Preflight method matching uses complete comma-separated method names."""

import pytest
from flask import Flask

from flask_cors import CORS, cross_origin


@pytest.mark.parametrize("integration", ["extension", "decorator"])
@pytest.mark.parametrize(
    ("methods", "requested", "allowed"),
    [
        (["UNLOCK"], "LOCK", False),
        ("UNLOCK", "LOCK", False),
        (["POST"], "POS", False),
        (["POST"], "OST", False),
        ("GET,POST", "ET", False),
        (["UNLOCK"], "UNLOCK", True),
        ("GET,POST", "GET", True),
        ("GET, POST", "POST", True),
        (["POST"], "post", True),
        (["POST"], "DELETE", False),
    ],
)
def test_preflight_requires_complete_method(integration, methods, requested, allowed):
    app = Flask(__name__)
    options = {"methods": methods, "allow_headers": ["X-Example"], "max_age": 60}

    def resource():
        return "ok"

    if integration == "extension":
        CORS(app, **options)
    else:
        resource = cross_origin(**options)(resource)
    app.add_url_rule("/resource", view_func=resource)

    response = app.test_client().options(
        "/resource",
        headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": requested,
            "Access-Control-Request-Headers": "X-Example",
        },
    )
    if allowed:
        assert requested.upper() in [
            method.strip() for method in response.headers["Access-Control-Allow-Methods"].split(",")
        ]
        assert response.headers["Access-Control-Allow-Headers"] == "X-Example"
        assert response.headers["Access-Control-Max-Age"] == "60"
    else:
        assert "Access-Control-Allow-Methods" not in response.headers
        assert "Access-Control-Allow-Headers" not in response.headers
        assert "Access-Control-Max-Age" not in response.headers
