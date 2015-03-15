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


class MethodsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return 'Should only return headers on pre-flight OPTIONS request'

        @self.app.route('/test_methods_defined')
        @cross_origin(methods=['POST'])
        def test_get():
            return 'Only allow POST'

    def test_defaults(self):
        ''' Access-Control-Allow-Methods headers should only be returned
            if the client makes an OPTIONS request.
        '''

        self.assertFalse(ACL_METHODS in self.get('/defaults', origin='www.example.com').headers)
        self.assertFalse(ACL_METHODS in self.head('/defaults', origin='www.example.com').headers)
        res = self.preflight('/defaults', 'POST', origin='www.example.com')
        for method in ALL_METHODS:
            self.assertTrue(method in res.headers.get(ACL_METHODS))

    def test_methods_defined(self):
        ''' If the methods parameter is defined, it should override the default
            methods defined by the user.
        '''
        self.assertFalse(ACL_METHODS in self.get('/test_methods_defined').headers)
        self.assertFalse(ACL_METHODS in self.head('/test_methods_defined').headers)

        res = self.preflight('/test_methods_defined', 'POST', origin='www.example.com')
        self.assertTrue('POST' in res.headers.get(ACL_METHODS))

        res = self.preflight('/test_methods_defined', 'PUT', origin='www.example.com')
        self.assertFalse(ACL_METHODS in res.headers)

        res = self.get('/test_methods_defined', origin='www.example.com')
        self.assertFalse(ACL_METHODS in res.headers)


class AppConfigMethodsTestCase(AppConfigTest, MethodsCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigMethodsTestCase, self).__init__(*args, **kwargs)

    def test_defaults(self):
        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return ''

        super(AppConfigMethodsTestCase, self).test_defaults()

    def test_methods_defined(self):
        self.app.config['CORS_METHODS'] = ['POST']

        @self.app.route('/test_methods_defined')
        @cross_origin()
        def defaults():
            return ''
        super(AppConfigMethodsTestCase, self).test_methods_defined()


if __name__ == "__main__":
    unittest.main()
