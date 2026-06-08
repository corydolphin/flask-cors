"""
test_blueprint
~~~~~~~~~~~~~~
Flask-CORS supports applying CORS configuration directly to a Flask
Blueprint, in addition to a whole application. Blueprints do not expose a
``config`` attribute or the ``handle_exception`` hooks, so these tests guard
that the extension keeps working when handed one.

:copyright: (c) 2016 by Cory Dolphin.
:license: MIT, see LICENSE for more details.
"""

from flask import Blueprint, Flask

from flask_cors import *
from flask_cors.core import *

from ..base_test import FlaskCorsTestCase


class BlueprintExtensionTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.bp = Blueprint("blueprint", __name__)
        CORS(self.bp, resources={r"/api/*": {"origins": "http://foo.com"}})

        @self.bp.route("/api/v1/ping")
        def ping():
            return "pong"

        @self.bp.route("/no_cors")
        def no_cors():
            return "no cors here"

        self.app = Flask(__name__)
        self.app.register_blueprint(self.bp)

    def test_blueprint_resource_has_cors(self):
        """Routes registered on a CORS-enabled blueprint and matching the
        configured resource should receive CORS headers.
        """
        resp = self.get("/api/v1/ping", origin="http://foo.com")
        self.assertEqual(resp.headers.get(ACL_ORIGIN), "http://foo.com")

    def test_blueprint_non_matching_route_has_no_cors(self):
        """Routes that do not match the configured resource should not have
        CORS headers set.
        """
        resp = self.get("/no_cors", origin="http://foo.com")
        self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_blueprint_init_app(self):
        """Blueprints should also be configurable via ``init_app``."""
        bp = Blueprint("blueprint_init", __name__)

        @bp.route("/api/v2/ping")
        def ping_v2():
            return "pong"

        cors = CORS(resources={r"/api/*": {"origins": "http://bar.com"}})
        cors.init_app(bp)

        self.app = Flask(__name__)
        self.app.register_blueprint(bp)

        resp = self.get("/api/v2/ping", origin="http://bar.com")
        self.assertEqual(resp.headers.get(ACL_ORIGIN), "http://bar.com")


if __name__ == "__main__":
    import unittest

    unittest.main()
