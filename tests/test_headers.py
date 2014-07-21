# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from tests.base_test import FlaskCorsTestCase
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *

class HeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_list')
        @cross_origin(headers=["Foo", "Bar"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(headers="Foo")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(headers=set(["Foo", "Bar"]))
        def test_set():
            return 'Welcome!'

    def test_app_configured_headers(self):
        ''' If the application contains a list of headers in the
            `CORS_HEADERS` config value, then headers should default to them.
        '''
        app = Flask(__name__)
        app.config['CORS_HEADERS'] = ['Foo', 'Bar']

        @app.route('/')
        @cross_origin(methods=['GET', 'OPTIONS', 'HEAD', 'PUT', 'POST'])
        def wildcard():
            return 'Welcome!'

        with app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertEqual(result.headers.get(ACL_HEADERS), 'Foo, Bar')

    def test_list_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_list')
            self.assertEqual(result.headers.get(ACL_HEADERS), 'Foo, Bar')

    def test_string_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_string')
            self.assertEqual(result.headers.get(ACL_HEADERS), 'Foo')

    def test_set_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_set')

            allowed = result.headers.get(ACL_HEADERS)
            # Order is not garaunteed for sets
            self.assertTrue(allowed in ['Foo, Bar', 'Bar, Foo'])


if __name__ == "__main__":
    unittest.main()
