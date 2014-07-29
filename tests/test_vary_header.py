# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

from tests.base_test import FlaskCorsTestCase
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class VaryHeaderTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

        @self.app.route('/test_vary')
        @cross_origin(origins=["Foo", "Bar"])
        def test_vary():
            return 'Welcome!'

        @self.app.route('/test_existing_vary_headers')
        @cross_origin(origins=["Foo", "Bar"])
        def test_existing_vary_headers():
            return 'Welcome!', 200, {'Vary': 'Accept-Encoding'}

    def test_consistent_origin(self):
        '''
            If the Access-Control-Allow-Origin header will not be changed
            dynamically, there is no need to Vary:Origin header should not
            be set.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertFalse('Vary' in result.headers)

    def test_varying_origin(self):
        ''' Resources that wish to enable themselves to be shared with
            multiple Origins but do not respond uniformly with "*" must
            in practice generate the Access-Control-Allow-Origin header
            dynamically in response to every request they wish to allow.

            As a consequence, authors of such resources should send a Vary:
            Origin HTTP header or provide other appropriate control directives
            to prevent caching of such responses, which may be inaccurate if
            re-used across-origins.
        '''
        example_origin = 'http://example.com'
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/test_vary', headers={'Origin': example_origin})
                self.assertEqual(result.headers.get('Vary'), 'Origin')

    def test_consistent_origin_concat(self):
        '''
            If Flask-Cors adds a Vary header and there is already a Vary
            header set, the headers should be combined and comma-separated.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/test_existing_vary_headers')
                self.assertEqual(
                    result.headers.get('Vary'),
                    'Origin, Accept-Encoding'
                )


if __name__ == "__main__":
    unittest.main()
