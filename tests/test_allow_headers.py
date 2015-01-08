# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from tests.base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class AllowHeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_override')
        @cross_origin(allow_headers=['X-Example-Header-B', 'X-Example-Header-A'])
        def test_override():
            return 'Welcome!'

        @self.app.route('/test_backwards_compatible')
        @cross_origin(headers=['X-Example-Header-B', 'X-Example-Header-A'])
        def test_list():
            return 'Welcome!'

    def test_default(self):
        for resp in self.iter_responses('/test_default'):
            self.assertTrue(resp.headers.get(ACL_ALLOW_HEADERS) is None,
                            "Default should have no allowed headers")

    def test_override(self):
        '''
            If there is an Access-Control-Request-Method header in the request
            and Access-Control-Request-Method is allowed for cross origin
            requests and request method is OPTIONS,
            the Access-Control-Allow-Headers header should be echoed back.
        '''
        resp = self.preflight('/test_override')
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS), 'X-Example-Header-A, X-Example-Header-B')

    def test_backwards_compatible(self):
        '''
            Version 1.10.2 changed the name of the parameter from 'headers'
            to 'allow_headers'
        '''
        resp = self.preflight('/test_backwards_compatible')
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS),
                         'X-Example-Header-A, X-Example-Header-B')

        for resp in self.iter_responses('/test_backwards_compatible',
                                        verbs=['HEAD', 'GET']):
            self.assertTrue(resp.headers.get(ACL_ALLOW_HEADERS) is None)


class AppConfigAllowHeadersTestCase(AppConfigTest, AllowHeadersTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigAllowHeadersTestCase, self).__init__(*args, **kwargs)

    def test_default(self):
        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'
        super(AppConfigAllowHeadersTestCase, self).test_default()

    def test_override(self):
        self.app.config['CORS_ALLOW_HEADERS'] = ['X-Example-Header-B',
                                                 'X-Example-Header-A']

        @self.app.route('/test_override')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigAllowHeadersTestCase, self).test_override()

    def test_backwards_compatible(self):
        '''
            Version 1.10.2 changed the name of the parameter from 'headers'
            to 'allow_headers'
        '''
        self.app.config['CORS_HEADERS'] = ['X-Example-Header-B',
                                           'X-Example-Header-A']

        @self.app.route('/test_backwards_compatible')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigAllowHeadersTestCase, self).test_backwards_compatible()


if __name__ == "__main__":
    unittest.main()