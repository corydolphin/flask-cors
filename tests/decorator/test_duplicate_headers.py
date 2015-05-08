# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from ..base_test import FlaskCorsTestCase
from flask import Flask, Response

from flask_cors import *
from flask_cors.core import *


class AllowsMultipleHeaderEntries(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_multiple_set_cookie_headers')
        @cross_origin()
        def test_multiple_set_cookie_headers():
            resp = Response("Foo bar baz")
            resp.headers.add('set-cookie', 'foo')
            resp.headers.add('set-cookie', 'bar')
            return resp

    def test_multiple_set_cookie_headers(self):
        resp = self.get('/test_multiple_set_cookie_headers')
        self.assertEqual(len(resp.headers.getlist('set-cookie')), 2)

if __name__ == "__main__":
    unittest.main()
