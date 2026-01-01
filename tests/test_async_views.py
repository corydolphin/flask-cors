"""
Tests for async view support in Flask-CORS.

This module tests that Flask-CORS correctly handles async view functions,
which are supported in Flask 2.0+. These tests verify that CORS headers
are properly applied to both sync and async views.
"""

import pytest
from flask import Flask

from flask_cors import CORS, cross_origin
from flask_cors.core import ACL_CREDENTIALS, ACL_METHODS, ACL_ORIGIN


class TestAsyncViewsWithExtension:
    """Test async views with the CORS extension."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with async views and CORS extension."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        CORS(app)

        @app.route("/sync")
        def sync_view() -> str:
            return "sync"

        @app.route("/async")
        async def async_view() -> str:
            return "async"

        @app.route("/async-await")
        async def async_view_with_await() -> str:
            import asyncio

            await asyncio.sleep(0)
            return "async-await"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_sync_view_returns_cors_headers(self, client) -> None:
        """Sync views should return CORS headers."""
        response = client.get("/sync", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.data == b"sync"
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_async_view_returns_cors_headers(self, client) -> None:
        """Async views should return CORS headers."""
        response = client.get("/async", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.data == b"async"
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_async_view_with_await_returns_cors_headers(self, client) -> None:
        """Async views with await should return CORS headers."""
        response = client.get(
            "/async-await", headers={"Origin": "http://example.com"}
        )
        assert response.status_code == 200
        assert response.data == b"async-await"
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_async_view_options_request(self, client) -> None:
        """Async views should handle OPTIONS preflight requests."""
        response = client.options(
            "/async",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"


class TestAsyncViewsWithDecorator:
    """Test async views with the @cross_origin decorator."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with async decorated views."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/sync")
        @cross_origin()
        def sync_view() -> str:
            return "sync"

        @app.route("/async")
        @cross_origin()
        async def async_view() -> str:
            return "async"

        @app.route("/async-await")
        @cross_origin()
        async def async_view_with_await() -> str:
            import asyncio

            await asyncio.sleep(0)
            return "async-await"

        @app.route("/async-custom")
        @cross_origin(origins=["http://allowed.com"], supports_credentials=True)
        async def async_custom() -> str:
            return "async-custom"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_sync_decorated_view(self, client) -> None:
        """Sync decorated views should return CORS headers."""
        response = client.get("/sync", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.data == b"sync"
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_async_decorated_view(self, client) -> None:
        """Async decorated views should return CORS headers."""
        response = client.get("/async", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert response.data == b"async"
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_async_decorated_view_with_await(self, client) -> None:
        """Async decorated views with await should return CORS headers."""
        response = client.get(
            "/async-await", headers={"Origin": "http://example.com"}
        )
        assert response.status_code == 200
        assert response.data == b"async-await"
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_async_decorated_view_custom_options(self, client) -> None:
        """Async decorated views should respect custom options."""
        # Request from allowed origin
        response = client.get(
            "/async-custom", headers={"Origin": "http://allowed.com"}
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://allowed.com"
        assert response.headers.get(ACL_CREDENTIALS) == "true"

        # Request from disallowed origin
        response = client.get(
            "/async-custom", headers={"Origin": "http://other.com"}
        )
        assert response.status_code == 200
        assert ACL_ORIGIN not in response.headers

    def test_async_decorated_options_request(self, client) -> None:
        """Async decorated views should handle OPTIONS preflight requests."""
        response = client.options(
            "/async",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"
        assert ACL_METHODS in response.headers


class TestAsyncViewsWithResourceConfig:
    """Test async views with resource-specific CORS configuration."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with resource-specific CORS config."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        CORS(
            app,
            resources={
                r"/api/*": {"origins": ["http://api-client.com"]},
                r"/public/*": {"origins": "*"},
            },
        )

        @app.route("/api/data")
        async def async_api() -> str:
            return "api-data"

        @app.route("/public/info")
        async def async_public() -> str:
            return "public-info"

        @app.route("/other")
        async def async_other() -> str:
            return "other"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_async_api_allowed_origin(self, client) -> None:
        """Async API endpoint should allow configured origin."""
        response = client.get(
            "/api/data", headers={"Origin": "http://api-client.com"}
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://api-client.com"

    def test_async_api_disallowed_origin(self, client) -> None:
        """Async API endpoint should reject unconfigured origin."""
        response = client.get("/api/data", headers={"Origin": "http://other.com"})
        assert response.status_code == 200
        assert ACL_ORIGIN not in response.headers

    def test_async_public_any_origin(self, client) -> None:
        """Async public endpoint should allow any origin."""
        response = client.get(
            "/public/info", headers={"Origin": "http://any-origin.com"}
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://any-origin.com"

    def test_async_unconfigured_route(self, client) -> None:
        """Async route not matching resources should not have CORS headers."""
        response = client.get("/other", headers={"Origin": "http://example.com"})
        assert response.status_code == 200
        assert ACL_ORIGIN not in response.headers


class TestAsyncViewsPreflightRequests:
    """Test preflight request handling for async views."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app for preflight testing."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/async-post", methods=["GET", "POST"])
        @cross_origin(methods=["GET", "POST"])
        async def async_post() -> str:
            return "async-post"

        @app.route("/async-custom-headers", methods=["GET", "POST"])
        @cross_origin(allow_headers=["X-Custom-Header", "Content-Type"])
        async def async_custom_headers() -> str:
            return "async-custom-headers"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_preflight_for_async_post(self, client) -> None:
        """Preflight request for async POST endpoint."""
        response = client.options(
            "/async-post",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"
        assert "POST" in response.headers.get(ACL_METHODS, "")

    def test_preflight_with_custom_headers(self, client) -> None:
        """Preflight request with custom headers for async endpoint."""
        response = client.options(
            "/async-custom-headers",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "X-Custom-Header, Content-Type",
            },
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"


class TestAsyncViewMixedWithSync:
    """Test mixed async and sync views in the same application."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with mixed sync and async views."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        CORS(app, origins=["http://example.com"])

        @app.route("/sync-1")
        def sync_1() -> str:
            return "sync-1"

        @app.route("/async-1")
        async def async_1() -> str:
            return "async-1"

        @app.route("/sync-2")
        def sync_2() -> str:
            return "sync-2"

        @app.route("/async-2")
        async def async_2() -> str:
            import asyncio

            await asyncio.sleep(0)
            return "async-2"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_interleaved_requests(self, client) -> None:
        """Mixed sync and async views should all return CORS headers."""
        for path in ["/sync-1", "/async-1", "/sync-2", "/async-2"]:
            response = client.get(path, headers={"Origin": "http://example.com"})
            assert response.status_code == 200
            assert response.headers.get(ACL_ORIGIN) == "http://example.com", (
                f"CORS header missing for {path}"
            )


class TestAsyncDecoratorPreservesMetadata:
    """Test that the decorator preserves async function metadata."""

    def test_wrapped_function_is_async(self) -> None:
        """The wrapped function should remain async."""
        import asyncio

        app = Flask(__name__)

        @app.route("/async")
        @cross_origin()
        async def async_view() -> str:
            return "async"

        # Get the view function from the app's URL map
        with app.test_request_context():
            view_func = app.view_functions["async_view"]
            assert asyncio.iscoroutinefunction(view_func)

    def test_function_name_preserved(self) -> None:
        """The wrapped function should preserve its name."""
        app = Flask(__name__)

        @app.route("/async")
        @cross_origin()
        async def my_async_view() -> str:
            return "async"

        view_func = app.view_functions["my_async_view"]
        assert view_func.__name__ == "my_async_view"

    def test_function_docstring_preserved(self) -> None:
        """The wrapped function should preserve its docstring."""
        app = Flask(__name__)

        @app.route("/async")
        @cross_origin()
        async def documented_view() -> str:
            """This is a documented async view."""
            return "async"

        view_func = app.view_functions["documented_view"]
        assert view_func.__doc__ == """This is a documented async view."""
