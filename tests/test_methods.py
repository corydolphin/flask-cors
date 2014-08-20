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


class MethodsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return 'Should only return headers on OPTIONS'

        @self.app.route('/get')
        @cross_origin(methods=['GET'])
        def test_get():
            return 'Get only!'

        @self.app.route('/all_methods', methods=ALL_METHODS)
        @cross_origin()
        def test_all_methods():
            return ''

    def test_defaults(self):
        ''' By default, Access-Control-Allow-Methods should only be returned
            if the client makes an OPTIONS request.
        '''

        self.assertFalse(ACL_METHODS in self.get('/defaults').headers)
        self.assertFalse(ACL_METHODS in self.head('/defaults').headers)
        self.assertTrue(ACL_METHODS in self.options('/defaults').headers)

    def test_methods_defined(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        for resp in self.iter_responses('/get'):
            self.assertTrue(ACL_METHODS in resp.headers)
            self.assertTrue('GET' in resp.headers[ACL_METHODS])

    def test_all_methods(self):
        for resp in self.iter_responses('/all_methods', verbs=ALL_METHODS):
            self.assertTrue(ACL_ORIGIN in resp.headers)


class AppConfigMethodsTestCase(AppConfigTest, MethodsCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigMethodsTestCase, self).__init__(*args, **kwargs)

    def test_defaults(self):
        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return 'Should only return headers on OPTIONS'

        super(AppConfigMethodsTestCase, self).test_defaults()

    def test_methods_defined(self):
        self.app.config['CORS_METHODS'] = ['GET']

        @self.app.route('/get')
        @cross_origin()
        def defaults():
            return 'Should only return headers on OPTIONS'

        super(AppConfigMethodsTestCase, self).test_methods_defined()

    def test_all_methods(self):
        @self.app.route('/all_methods', methods=ALL_METHODS)
        @cross_origin()
        def test_all_methods():
            return ''

        super(AppConfigMethodsTestCase, self).test_all_methods()


if __name__ == "__main__":
    unittest.main()
