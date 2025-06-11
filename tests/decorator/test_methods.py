# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2016 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

from ..base_test import FlaskCorsTestCase
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

        @self.app.route('/defaults_async')
        @cross_origin()
        async def defaults_async():
            return 'Should only return headers on pre-flight OPTIONS request'

        @self.app.route('/test_methods_defined_async')
        @cross_origin(methods=['POST'])
        async def test_get_async():
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

        self.assertFalse(ACL_METHODS in self.get('/defaults_async', origin='www.example.com').headers)
        self.assertFalse(ACL_METHODS in self.head('/defaults_async', origin='www.example.com').headers)
        res = self.preflight('/defaults_async', 'POST', origin='www.example.com')
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

        self.assertFalse(ACL_METHODS in self.get('/test_methods_defined_async').headers)
        self.assertFalse(ACL_METHODS in self.head('/test_methods_defined_async').headers)

        res = self.preflight('/test_methods_defined_async', 'POST', origin='www.example.com')
        self.assertTrue('POST' in res.headers.get(ACL_METHODS))

        res = self.preflight('/test_methods_defined_async', 'PUT', origin='www.example.com')
        self.assertFalse(ACL_METHODS in res.headers)

        res = self.get('/test_methods_defined_async', origin='www.example.com')
        self.assertFalse(ACL_METHODS in res.headers)

if __name__ == "__main__":
    unittest.main()
