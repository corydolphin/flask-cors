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
from flask import Flask, Response

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
        @cross_origin(origins=["http://foo.com", "http://bar.com"])
        def test_vary():
            return 'Welcome!'

        @self.app.route('/test_existing_vary_headers')
        @cross_origin(origins=["http://foo.com", "http://bar.com"])
        def test_existing_vary_headers():
            return Response('', status=200,
                            headers={'Vary': 'Accept-Encoding'})

    def test_consistent_origin(self):
        '''
            If the Access-Control-Allow-Origin header will not be changed
            dynamically, there is no need to Vary:Origin header should not
            be set.
        '''
        for resp in self.iter_responses('/'):
            self.assertFalse('Vary' in resp.headers)

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
        example_origin = 'http://foo.com'
        for resp in self.iter_responses('/test_vary',
                                        headers={'Origin': example_origin}):
            self.assertEqual(resp.headers.get('Vary'), 'Origin')

    def test_consistent_origin_concat(self):
        '''
            If Flask-Cors adds a Vary header and there is already a Vary
            header set, the headers should be combined and comma-separated.
        '''

        resp = self.get('/test_existing_vary_headers')
        self.assertEqual(
            resp.headers.get('Vary'),
            'Origin, Accept-Encoding'
        )


class AppConfigVaryHeaderTestCase(AppConfigTest,
                                  VaryHeaderTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigVaryHeaderTestCase, self).__init__(*args, **kwargs)

    def test_consistent_origin(self):
        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

        super(AppConfigVaryHeaderTestCase, self).test_consistent_origin()

    def test_varying_origin(self):
        self.app.config['CORS_ORIGINS'] = ["http://foo.com", "http://bar.com"]

        @self.app.route('/test_vary')
        @cross_origin()
        def test_vary():
            return 'Welcome!'

        super(AppConfigVaryHeaderTestCase, self).test_varying_origin()

    def test_consistent_origin_concat(self):
        self.app.config['CORS_ORIGINS'] = ["http://foo.com", "http://bar.com"]

        @self.app.route('/test_existing_vary_headers')
        @cross_origin()
        def test_existing_vary_headers():
            return Response('', status=200,
                            headers={'Vary': 'Accept-Encoding'})

        super(AppConfigVaryHeaderTestCase, self).test_consistent_origin_concat()


if __name__ == "__main__":
    unittest.main()
