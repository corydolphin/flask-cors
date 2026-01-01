"""
Pytest configuration and fixtures for Flask-CORS tests.

This module provides modern pytest fixtures that can be used alongside
the existing unittest-based tests, enabling a gradual migration to
pytest-style testing.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING, Any, ClassVar

import pytest
from flask import Flask
from flask.testing import FlaskClient

from flask_cors import CORS, cross_origin
from flask_cors.core import ACL_ORIGIN

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.fixture
def app() -> Flask:
    """Create a basic Flask application for testing."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def cors_app() -> Flask:
    """Create a Flask application with CORS enabled for all routes."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    CORS(app)

    @app.route("/")
    def index() -> str:
        return "Welcome!"

    @app.route("/api/resource")
    def api_resource() -> str:
        return "API Resource"

    return app


@pytest.fixture
def cors_client(cors_app: Flask) -> FlaskClient:
    """Create a test client for a CORS-enabled Flask application."""
    return cors_app.test_client()


@pytest.fixture
def make_app() -> Callable[..., Flask]:
    """Factory fixture to create Flask apps with custom configurations."""

    def _make_app(**cors_options: Any) -> Flask:
        app = Flask(__name__)
        app.config["TESTING"] = True

        if cors_options:
            CORS(app, **cors_options)

        return app

    return _make_app


@pytest.fixture
def make_decorated_app() -> Callable[..., Flask]:
    """Factory fixture to create Flask apps with decorated routes."""

    def _make_decorated_app(
        decorator_options: dict[str, Any] | None = None,
    ) -> Flask:
        app = Flask(__name__)
        app.config["TESTING"] = True

        opts = decorator_options or {}

        @app.route("/")
        @cross_origin(**opts)
        def index() -> str:
            return "Welcome!"

        return app

    return _make_decorated_app


class CORSTestHelper:
    """Helper class providing common test utilities for CORS testing."""

    HTTP_METHODS: ClassVar[list[str]] = ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"]

    def __init__(self, client: FlaskClient) -> None:
        self.client = client

    def request(
        self,
        method: str,
        path: str,
        origin: str | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Make a request with optional Origin header."""
        request_headers = headers.copy() if headers else {}
        if origin:
            request_headers["Origin"] = origin

        method_func = getattr(self.client, method.lower())
        return method_func(path, headers=request_headers, **kwargs)

    def get(self, path: str, **kwargs: Any) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Any:
        return self.request("POST", path, **kwargs)

    def options(self, path: str, **kwargs: Any) -> Any:
        return self.request("OPTIONS", path, **kwargs)

    def preflight(
        self,
        path: str,
        method: str = "GET",
        origin: str | None = None,
        request_headers: list[str] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Make a CORS preflight request."""
        headers = kwargs.pop("headers", {})
        headers["Access-Control-Request-Method"] = method

        if request_headers:
            headers["Access-Control-Request-Headers"] = ", ".join(request_headers)

        return self.options(path, origin=origin, headers=headers, **kwargs)

    def iter_responses(
        self,
        path: str,
        methods: list[str] | None = None,
        **kwargs: Any,
    ) -> Generator[Any, None, None]:
        """Iterate over responses for multiple HTTP methods."""
        methods = methods or ["GET", "HEAD", "OPTIONS"]
        for method in methods:
            yield self.request(method, path, **kwargs)

    def assert_cors_origin(
        self,
        response: Any,
        expected_origin: str | None = None,
    ) -> None:
        """Assert that the response has the expected CORS origin header."""
        if expected_origin is None:
            assert ACL_ORIGIN in response.headers
        else:
            assert response.headers.get(ACL_ORIGIN) == expected_origin

    def assert_no_cors_origin(self, response: Any) -> None:
        """Assert that the response does not have a CORS origin header."""
        assert ACL_ORIGIN not in response.headers


@pytest.fixture
def cors_helper(client: FlaskClient) -> CORSTestHelper:
    """Create a CORS test helper for the test client."""
    return CORSTestHelper(client)


@pytest.fixture
def cors_app_helper(cors_client: FlaskClient) -> CORSTestHelper:
    """Create a CORS test helper for the CORS-enabled test client."""
    return CORSTestHelper(cors_client)


# Async fixtures for testing async views (Flask 2.0+)
@pytest.fixture
def async_app() -> Flask:
    """Create a Flask application with async views and CORS enabled."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    CORS(app)

    @app.route("/sync")
    def sync_view() -> str:
        return "Sync response"

    @app.route("/async")
    async def async_view() -> str:
        return "Async response"

    @app.route("/async-with-await")
    async def async_view_with_await() -> str:
        import asyncio

        await asyncio.sleep(0)
        return "Async with await response"

    return app


@pytest.fixture
def async_client(async_app: Flask) -> FlaskClient:
    """Create a test client for an async Flask application."""
    return async_app.test_client()


@pytest.fixture
def async_decorated_app() -> Flask:
    """Create a Flask application with async decorated views."""
    app = Flask(__name__)
    app.config["TESTING"] = True

    @app.route("/sync")
    @cross_origin()
    def sync_view() -> str:
        return "Sync response"

    @app.route("/async")
    @cross_origin()
    async def async_view() -> str:
        return "Async response"

    @app.route("/async-custom-origins")
    @cross_origin(origins=["http://example.com"])
    async def async_custom_origins() -> str:
        return "Async custom origins"

    return app


@pytest.fixture
def async_decorated_client(async_decorated_app: Flask) -> FlaskClient:
    """Create a test client for an async decorated Flask application."""
    return async_decorated_app.test_client()
