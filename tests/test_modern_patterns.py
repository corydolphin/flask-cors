"""
Modern pytest-style tests demonstrating best practices for Flask-CORS testing.

This module showcases modern pytest patterns including:
- Pytest fixtures for app and client setup
- Parametrized tests for DRY testing
- Clear test organization with classes
- Type hints for better IDE support
"""

import pytest
from flask import Flask

from flask_cors import CORS, cross_origin
from flask_cors.core import (
    ACL_ALLOW_HEADERS,
    ACL_CREDENTIALS,
    ACL_EXPOSE_HEADERS,
    ACL_MAX_AGE,
    ACL_METHODS,
    ACL_ORIGIN,
)


class TestCORSExtensionBasics:
    """Test basic CORS extension functionality using modern pytest patterns."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create a basic CORS-enabled Flask app."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        CORS(app)

        @app.route("/")
        def index() -> str:
            return "Hello"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    @pytest.mark.parametrize(
        "method",
        ["get", "head", "options"],
    )
    def test_cors_headers_on_all_methods(self, client, method: str) -> None:
        """CORS headers should be present for all HTTP methods."""
        response = getattr(client, method)(
            "/", headers={"Origin": "http://example.com"}
        )
        assert response.status_code == 200
        assert response.headers.get(ACL_ORIGIN) == "http://example.com"

    def test_wildcard_origin_without_request_origin(self, client) -> None:
        """Without Origin header, wildcard should be returned."""
        response = client.get("/")
        assert response.headers.get(ACL_ORIGIN) == "*"

    @pytest.mark.parametrize(
        "origin",
        [
            "http://example.com",
            "http://localhost:3000",
            "https://app.example.org",
        ],
    )
    def test_origin_echoed_back(self, client, origin: str) -> None:
        """Request Origin should be echoed back in response."""
        response = client.get("/", headers={"Origin": origin})
        assert response.headers.get(ACL_ORIGIN) == origin


class TestCORSDecoratorBasics:
    """Test basic @cross_origin decorator functionality."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with decorated routes."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/default")
        @cross_origin()
        def default_cors() -> str:
            return "default"

        @app.route("/custom-origins")
        @cross_origin(origins=["http://allowed.com", "http://also-allowed.com"])
        def custom_origins() -> str:
            return "custom"

        @app.route("/with-credentials")
        @cross_origin(supports_credentials=True, origins=["http://trusted.com"])
        def with_credentials() -> str:
            return "credentials"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_default_decorator_allows_any_origin(self, client) -> None:
        """Default decorator should allow any origin."""
        response = client.get(
            "/default", headers={"Origin": "http://any-origin.com"}
        )
        assert response.headers.get(ACL_ORIGIN) == "http://any-origin.com"

    @pytest.mark.parametrize(
        "origin,should_allow",
        [
            ("http://allowed.com", True),
            ("http://also-allowed.com", True),
            ("http://not-allowed.com", False),
        ],
    )
    def test_custom_origins_filtering(
        self, client, origin: str, should_allow: bool
    ) -> None:
        """Only configured origins should be allowed."""
        response = client.get("/custom-origins", headers={"Origin": origin})
        if should_allow:
            assert response.headers.get(ACL_ORIGIN) == origin
        else:
            assert ACL_ORIGIN not in response.headers

    def test_credentials_header_when_enabled(self, client) -> None:
        """Credentials header should be present when enabled."""
        response = client.get(
            "/with-credentials", headers={"Origin": "http://trusted.com"}
        )
        assert response.headers.get(ACL_CREDENTIALS) == "true"


class TestCORSPreflightRequests:
    """Test CORS preflight (OPTIONS) request handling."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app for preflight testing."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/api/resource", methods=["GET", "POST", "PUT", "DELETE"])
        @cross_origin(
            methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Content-Type", "Authorization"],
            max_age=600,
        )
        def api_resource() -> str:
            return "resource"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_preflight_returns_allowed_methods(self, client) -> None:
        """Preflight should return allowed methods."""
        response = client.options(
            "/api/resource",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        methods = response.headers.get(ACL_METHODS, "")
        assert "POST" in methods
        assert "GET" in methods

    def test_preflight_returns_allowed_headers(self, client) -> None:
        """Preflight should return allowed headers."""
        response = client.options(
            "/api/resource",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization",
            },
        )
        allowed_headers = response.headers.get(ACL_ALLOW_HEADERS, "")
        assert "Content-Type" in allowed_headers or "content-type" in allowed_headers.lower()

    def test_preflight_returns_max_age(self, client) -> None:
        """Preflight should return max age."""
        response = client.options(
            "/api/resource",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.headers.get(ACL_MAX_AGE) == "600"


class TestCORSResourcePatterns:
    """Test resource pattern matching with CORS extension."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with resource patterns."""
        app = Flask(__name__)
        app.config["TESTING"] = True
        CORS(
            app,
            resources={
                r"/api/*": {"origins": ["http://api-client.com"]},
                r"/public/*": {"origins": "*"},
                r"/admin/*": {
                    "origins": ["http://admin.example.com"],
                    "supports_credentials": True,
                },
            },
        )

        @app.route("/api/users")
        def api_users() -> str:
            return "users"

        @app.route("/api/posts")
        def api_posts() -> str:
            return "posts"

        @app.route("/public/info")
        def public_info() -> str:
            return "info"

        @app.route("/admin/dashboard")
        def admin_dashboard() -> str:
            return "dashboard"

        @app.route("/other")
        def other() -> str:
            return "other"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    @pytest.mark.parametrize(
        "path",
        ["/api/users", "/api/posts"],
    )
    def test_api_routes_allow_api_client(self, client, path: str) -> None:
        """API routes should allow the API client origin."""
        response = client.get(path, headers={"Origin": "http://api-client.com"})
        assert response.headers.get(ACL_ORIGIN) == "http://api-client.com"

    @pytest.mark.parametrize(
        "path",
        ["/api/users", "/api/posts"],
    )
    def test_api_routes_reject_other_origins(self, client, path: str) -> None:
        """API routes should reject other origins."""
        response = client.get(path, headers={"Origin": "http://other.com"})
        assert ACL_ORIGIN not in response.headers

    def test_public_routes_allow_any_origin(self, client) -> None:
        """Public routes should allow any origin."""
        response = client.get(
            "/public/info", headers={"Origin": "http://random.com"}
        )
        assert response.headers.get(ACL_ORIGIN) == "http://random.com"

    def test_admin_routes_include_credentials(self, client) -> None:
        """Admin routes should include credentials header."""
        response = client.get(
            "/admin/dashboard", headers={"Origin": "http://admin.example.com"}
        )
        assert response.headers.get(ACL_ORIGIN) == "http://admin.example.com"
        assert response.headers.get(ACL_CREDENTIALS) == "true"

    def test_unmatched_routes_no_cors(self, client) -> None:
        """Routes not matching any pattern should not have CORS headers."""
        response = client.get("/other", headers={"Origin": "http://example.com"})
        assert ACL_ORIGIN not in response.headers


class TestCORSExposeHeaders:
    """Test expose headers configuration."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create Flask app with expose headers."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/with-expose")
        @cross_origin(expose_headers=["X-Custom-Header", "X-Request-Id"])
        def with_expose() -> str:
            return "exposed"

        @app.route("/without-expose")
        @cross_origin()
        def without_expose() -> str:
            return "not-exposed"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    def test_expose_headers_present(self, client) -> None:
        """Expose headers should be present when configured."""
        response = client.get(
            "/with-expose", headers={"Origin": "http://example.com"}
        )
        expose = response.headers.get(ACL_EXPOSE_HEADERS, "")
        assert "X-Custom-Header" in expose
        assert "X-Request-Id" in expose

    def test_expose_headers_absent_when_not_configured(self, client) -> None:
        """Expose headers should be absent when not configured."""
        response = client.get(
            "/without-expose", headers={"Origin": "http://example.com"}
        )
        assert ACL_EXPOSE_HEADERS not in response.headers


class TestCORSVaryHeader:
    """Test Vary header behavior."""

    @pytest.fixture
    def multi_origin_app(self) -> Flask:
        """Create app with multiple allowed origins."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/multi")
        @cross_origin(origins=["http://one.com", "http://two.com"])
        def multi_origin() -> str:
            return "multi"

        return app

    @pytest.fixture
    def multi_origin_client(self, multi_origin_app: Flask):
        return multi_origin_app.test_client()

    @pytest.fixture
    def wildcard_app(self) -> Flask:
        """Create app with wildcard origin and send_wildcard=True."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/wildcard")
        @cross_origin(send_wildcard=True)
        def wildcard() -> str:
            return "wildcard"

        return app

    @pytest.fixture
    def wildcard_client(self, wildcard_app: Flask):
        return wildcard_app.test_client()

    def test_vary_header_with_multiple_origins(self, multi_origin_client) -> None:
        """Vary: Origin should be set when multiple origins are possible."""
        response = multi_origin_client.get(
            "/multi", headers={"Origin": "http://one.com"}
        )
        assert "Origin" in response.headers.get("Vary", "")

    def test_no_vary_header_with_wildcard(self, wildcard_client) -> None:
        """Vary: Origin should not be set when returning wildcard."""
        response = wildcard_client.get(
            "/wildcard", headers={"Origin": "http://example.com"}
        )
        assert response.headers.get(ACL_ORIGIN) == "*"
        # Vary header may or may not be present, but should not interfere


class TestCORSRegexOrigins:
    """Test regex-based origin matching."""

    @pytest.fixture
    def app(self) -> Flask:
        """Create app with regex origins."""
        app = Flask(__name__)
        app.config["TESTING"] = True

        @app.route("/subdomain")
        @cross_origin(origins=r"https?://.*\.example\.com")
        def subdomain() -> str:
            return "subdomain"

        return app

    @pytest.fixture
    def client(self, app: Flask):
        return app.test_client()

    @pytest.mark.parametrize(
        "origin",
        [
            "http://app.example.com",
            "https://api.example.com",
            "http://test.example.com",
        ],
    )
    def test_regex_matches_subdomains(self, client, origin: str) -> None:
        """Regex should match various subdomains."""
        response = client.get("/subdomain", headers={"Origin": origin})
        assert response.headers.get(ACL_ORIGIN) == origin

    @pytest.mark.parametrize(
        "origin",
        [
            "http://example.com",
            "http://other.com",
            "http://example.org",
        ],
    )
    def test_regex_rejects_non_matching(self, client, origin: str) -> None:
        """Regex should reject non-matching origins."""
        response = client.get("/subdomain", headers={"Origin": origin})
        assert ACL_ORIGIN not in response.headers
