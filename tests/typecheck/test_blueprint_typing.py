"""
test_blueprint_typing
~~~~~~~~~~~~~~~~~~~~~~
Static-typing regression test: ``CORS``/``init_app`` must keep accepting a
``Blueprint`` as well as a ``Flask`` app. ``tests/typecheck`` is checked by
mypy (strict) in CI, so narrowing the signature back to ``Flask`` only --
as in https://github.com/corydolphin/flask-cors/issues/410 -- fails here.

These functions exist only to be analyzed statically; they are not run.
"""

from __future__ import annotations

from flask import Blueprint, Flask

from flask_cors import CORS


def supports_flask_app() -> None:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://example.com"}})
    CORS().init_app(app)


def supports_blueprint() -> None:
    bp = Blueprint("api", __name__)
    # Must type-check: a Blueprint is a valid target for CORS.
    CORS(bp, resources={r"/api/*": {"origins": "http://example.com"}})
    CORS().init_app(bp)


def supports_no_app() -> None:
    CORS()
