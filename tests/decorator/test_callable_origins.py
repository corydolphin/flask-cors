"""
test_callable_origins
~~~~~~~~~~~~~~~~~~~~~
Tests for callable origins support in Flask-CORS.

:copyright: (c) 2024 by Cory Dolphin.
:license: MIT, see LICENSE for more details.
"""

from flask import Flask

from flask_cors import cross_origin
from flask_cors.core import ACL_ORIGIN

from ..base_test import FlaskCorsTestCase


class CallableOriginsTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        # Simple callable that returns a static list
        def static_origins(request_origin):
            return ["http://foo.com", "http://bar.com"]

        # Callable that validates against a whitelist
        def whitelist_origins(request_origin):
            allowed = {"http://foo.com", "http://bar.com"}
            if request_origin in allowed:
                return request_origin
            return None

        # Callable that returns wildcard
        def wildcard_origins(request_origin):
            return "*"

        @self.app.route("/test_callable_static")
        @cross_origin(origins=static_origins)
        def test_callable_static():
            return "Welcome!"

        @self.app.route("/test_callable_whitelist")
        @cross_origin(origins=whitelist_origins)
        def test_callable_whitelist():
            return "Welcome!"

        @self.app.route("/test_callable_wildcard")
        @cross_origin(origins=wildcard_origins, send_wildcard=True)
        def test_callable_wildcard():
            return "Welcome!"

    def test_callable_static_with_matching_origin(self):
        """Callable returning static list should allow matching origins."""
        for resp in self.iter_responses("/test_callable_static", origin="http://foo.com"):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), "http://foo.com")

    def test_callable_static_with_non_matching_origin(self):
        """Callable returning static list should reject non-matching origins."""
        for resp in self.iter_responses("/test_callable_static", origin="http://evil.com"):
            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(resp.headers.get(ACL_ORIGIN))

    def test_callable_whitelist_with_matching_origin(self):
        """Callable that validates against whitelist should allow matching origins."""
        for resp in self.iter_responses("/test_callable_whitelist", origin="http://bar.com"):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), "http://bar.com")

    def test_callable_whitelist_with_non_matching_origin(self):
        """Callable returning None should reject the origin."""
        for resp in self.iter_responses("/test_callable_whitelist", origin="http://evil.com"):
            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(resp.headers.get(ACL_ORIGIN))

    def test_callable_wildcard(self):
        """Callable returning wildcard should send '*'."""
        for resp in self.iter_responses("/test_callable_wildcard", origin="http://any.com"):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), "*")

    def test_callable_vary_header(self):
        """Callable origins should always include Vary header."""
        for resp in self.iter_responses("/test_callable_whitelist", origin="http://foo.com"):
            self.assertIn("Origin", resp.headers.get("Vary", ""))


class CallableOriginsExtensionTestCase(FlaskCorsTestCase):
    """Test callable origins with the CORS extension (app-wide)."""

    def setUp(self):
        self.app = Flask(__name__)

        def dynamic_origins(request_origin):
            # Simulate database lookup
            allowed = {"http://app1.example.com", "http://app2.example.com"}
            if request_origin in allowed:
                return request_origin
            return None

        from flask_cors import CORS

        CORS(self.app, origins=dynamic_origins)

        @self.app.route("/")
        def index():
            return "Hello!"

    def test_extension_callable_allowed(self):
        """Extension with callable origins should allow matching origins."""
        for resp in self.iter_responses("/", origin="http://app1.example.com"):
            self.assertEqual(resp.headers.get(ACL_ORIGIN), "http://app1.example.com")

    def test_extension_callable_denied(self):
        """Extension with callable origins should reject non-matching origins."""
        for resp in self.iter_responses("/", origin="http://evil.com"):
            self.assertIsNone(resp.headers.get(ACL_ORIGIN))
