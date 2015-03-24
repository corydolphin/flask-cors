# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

from ..base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

from flask_cors import *
from flask_cors.core import *


class SupportsCredentialsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_credentials_supported')
        @cross_origin(supports_credentials=True)
        def test_credentials_supported():
            return 'Credentials!'

        @self.app.route('/test_credentials_unsupported')
        @cross_origin(supports_credentials=False)
        def test_credentials_unsupported():
            return 'Credentials!'

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Open!'

    def test_credentials_supported(self):
        ''' The specified route should return the
            Access-Control-Allow-Credentials header.
        '''
        resp = self.get('/test_credentials_supported', origin='www.example.com')
        self.assertEquals(resp.headers.get(ACL_CREDENTIALS), 'true')

        resp = self.get('/test_credentials_supported')
        self.assertEquals(resp.headers.get(ACL_CREDENTIALS), None )

    def test_default(self):
        ''' The default behavior should be to disallow credentials.
        '''
        resp = self.get('/test_default', origin='www.example.com')
        self.assertFalse(ACL_CREDENTIALS in resp.headers)

        resp = self.get('/test_default')
        self.assertFalse(ACL_CREDENTIALS in resp.headers)

    def test_credentials_unsupported(self):
        ''' The default behavior should be to disallow credentials.
        '''
        resp = self.get('/test_credentials_unsupported', origin='www.example.com')
        self.assertFalse(ACL_CREDENTIALS in resp.headers)

        resp = self.get('/test_credentials_unsupported')
        self.assertFalse(ACL_CREDENTIALS in resp.headers)


class AppConfigExposeHeadersTestCase(AppConfigTest, SupportsCredentialsCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigExposeHeadersTestCase, self).__init__(*args, **kwargs)

    def test_credentials_supported(self):
        self.app.config['CORS_SUPPORTS_CREDENTIALS'] = True

        @self.app.route('/test_credentials_supported')
        @cross_origin()
        def test_credentials_supported():
            return 'Credentials!'

        super(AppConfigExposeHeadersTestCase, self).test_credentials_supported()

    def test_open_request(self):
        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Open!'
        super(AppConfigExposeHeadersTestCase, self).test_default()

if __name__ == "__main__":
    unittest.main()
