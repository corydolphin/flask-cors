# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

from tests.base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class SupportsCredentialsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_credentials')
        @cross_origin(supports_credentials=True)
        def test_credentials():
            return 'Credentials!'

        @self.app.route('/test_open')
        @cross_origin()
        def test_open():
            return 'Open!'

    def test_credentialed_request(self):
        ''' The specified route should return the
            Access-Control-Allow-Credentials header.
        '''
        resp = self.get('/test_credentials')
        header = resp.headers.get(ACL_CREDENTIALS)
        self.assertEquals(header, 'true')

    def test_open_request(self):
        ''' The default behavior should be to disallow credentials.
        '''
        resp = self.get('/test_open')
        self.assertTrue(ACL_CREDENTIALS not in resp.headers)


class AppConfigExposeHeadersTestCase(AppConfigTest, SupportsCredentialsCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigExposeHeadersTestCase, self).__init__(*args, **kwargs)

    def test_credentialed_request(self):
        self.app.config['CORS_SUPPORTS_CREDENTIALS'] = True

        @self.app.route('/test_credentials')
        @cross_origin()
        def test_credentials():
            return 'Credentials!'

        super(AppConfigExposeHeadersTestCase, self).test_credentialed_request()

    def test_open_request(self):
        @self.app.route('/test_open')
        @cross_origin()
        def test_open():
            return 'Open!'
        super(AppConfigExposeHeadersTestCase, self).test_open_request()

if __name__ == "__main__":
    unittest.main()
