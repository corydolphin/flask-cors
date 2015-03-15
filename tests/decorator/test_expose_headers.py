# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from ..base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

from flask_cors import *
from flask_cors.core import *


class ExposeHeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_override')
        @cross_origin(expose_headers=["X-My-Custom-Header", "X-Another-Custom-Header"])
        def test_override():
            return 'Welcome!'

    def test_default(self):
        for resp in self.iter_responses('/test_default', origin='www.example.com'):
            self.assertTrue(resp.headers.get(ACL_EXPOSE_HEADERS) is None,
                            "No Access-Control-Expose-Headers by default")

    def test_override(self):
        ''' The specified headers should be returned in the ACL_EXPOSE_HEADERS
            and correctly serialized if it is a list.
        '''
        for resp in self.iter_responses('/test_override', origin='www.example.com'):
            self.assertEqual(resp.headers.get(ACL_EXPOSE_HEADERS),
                             'X-Another-Custom-Header, X-My-Custom-Header')


class AppConfigExposeHeadersTestCase(AppConfigTest, ExposeHeadersTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigExposeHeadersTestCase, self).__init__(*args, **kwargs)

    def test_default(self):
        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        super(AppConfigExposeHeadersTestCase, self).test_default()

    def test_override(self):
        self.app.config['CORS_EXPOSE_HEADERS'] = ["X-My-Custom-Header",
                                                  "X-Another-Custom-Header"]

        @self.app.route('/test_override')
        @cross_origin()
        def test_override():
            return 'Welcome!'

        super(AppConfigExposeHeadersTestCase, self).test_override()


if __name__ == "__main__":
    unittest.main()
