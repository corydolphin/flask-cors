"""
test
~~~~
Flask-CORS is a simple extension to Flask allowing you to support cross
origin resource sharing (CORS) using a simple decorator.

:copyright: (c) 2016 by Cory Dolphin.
:license: MIT, see LICENSE for more details.
"""

from flask import Flask

from flask_cors import *
from flask_cors.core import *

from ..base_test import FlaskCorsTestCase


class OptionsTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route("/test_default")
        @cross_origin()
        def test_default():
            return "Welcome!"

        @self.app.route("/test_no_options_and_not_auto")
        @cross_origin(automatic_options=False)
        def test_no_options_and_not_auto():
            return "Welcome!"

        @self.app.route("/test_options_and_not_auto", methods=["OPTIONS"])
        @cross_origin(automatic_options=False)
        def test_options_and_not_auto():
            return "Welcome!"

    def test_defaults(self):
        """
        The default behavior should automatically provide OPTIONS
        and return CORS headers.
        """
        resp = self.options("/test_default", origin="http://foo.bar.com")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)

        resp = self.options("/test_default", origin="http://foo.bar.com")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)

    def test_no_options_and_not_auto(self):
        """
        If automatic_options is False, and the view func does not provide
        OPTIONS, then Flask's default handling will occur, and no CORS
        headers will be returned.
        """
        resp = self.options("/test_no_options_and_not_auto")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(ACL_ORIGIN in resp.headers)

        resp = self.options("/test_no_options_and_not_auto", origin="http://foo.bar.com")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_options_and_not_auto(self):
        """
        If OPTIONS is in methods, and automatic_options is False,
        the view function must return a response.
        """
        resp = self.options("/test_options_and_not_auto", origin="http://foo.bar.com")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)
        self.assertEqual(resp.data.decode("utf-8"), "Welcome!")

        resp = self.options("/test_options_and_not_auto", origin="http://foo.bar.com")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)
        self.assertEqual(resp.data.decode("utf-8"), "Welcome!")


if __name__ == "__main__":
    unittest.main()
