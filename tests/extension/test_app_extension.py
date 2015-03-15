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
from flask import Flask, jsonify

from flask_cors import *
from flask_cors.core import *


class AppExtensionRegexp(AppConfigTest):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={
            r'/': {},
            r'/test_list': {'origins': ["http://foo.com", "http://bar.com"]},
            r'/test_string': {'origins': 'http://foo.com'},
            r'/test_set': {
                'origins': set(["http://foo.com", "http://bar.com"])
            },
            r'/test_subdomain_regex': {
                'origins': r"http?://\w*\.?example\.com:?\d*/?.*"
            },
            r'/test_regex_list': {
                'origins': [r".*.example.com", r".*.otherexample.com"]
            },
            r'/test_regex_mixed_list': {
                'origins': ["http://example.com", r".*.otherexample.com"]
            },
            r'/test_send_wildcard_with_origin' : {
                'send_wildcard':True
            }
        })

        @self.app.route('/')
        def wildcard():
            return 'Welcome!'

        @self.app.route('/test_send_wildcard_with_origin')
        def send_wildcard_with_origin():
            return 'Welcome!'

        @self.app.route('/test_list')
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        def test_set():
            return 'Welcome!'

    def test_defaults_no_origin(self):
        ''' If there is no Origin header in the request, the
            Access-Control-Allow-Origin header should not be included,
            according to the w3 spec.
        '''
        for resp in self.iter_responses('/'):
            self.assertEqual(resp.headers.get(ACL_ORIGIN), None)

    def test_defaults_with_origin(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be included.
        '''
        for resp in self.iter_responses('/', origin='http://example.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://example.com')

    def test_send_wildcard_with_origin(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be included.
        '''
        for resp in self.iter_responses('/test_send_wildcard_with_origin', origin='http://example.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), '*')

    def test_list_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed.
        '''
        resp = self.get('/test_list', origin='http://bar.com')
        self.assertEqual(resp.headers.get(ACL_ORIGIN),'http://bar.com')

    def test_string_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        resp = self.get('/test_string', origin='http://foo.com')
        self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://foo.com')

    def test_set_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        resp = self.get('/test_set', origin='http://bar.com')

        allowed = resp.headers.get(ACL_ORIGIN)
        # Order is not garaunteed
        self.assertEqual(allowed, 'http://bar.com')

    def test_not_matching_origins(self):
        for resp in self.iter_responses('/test_list',origin="http://bazz.com"):
            self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_subdomain_regex(self):
        for sub in letters:
            domain = "http://%s.example.com" % sub
            for resp in self.iter_responses('/test_subdomain_regex',
                                            headers={'origin': domain}):
                self.assertEqual(domain, resp.headers.get(ACL_ORIGIN))

    def test_compiled_subdomain_regex(self):
        for sub in letters:
            domain = "http://%s.example.com" % sub
            for resp in self.iter_responses('/test_compiled_subdomain_regex',
                                            headers={'origin': domain}):
                self.assertEqual(domain, resp.headers.get(ACL_ORIGIN))

    def test_regex_list(self):
        for parent in 'example.com', 'otherexample.com':
            for sub in letters:
                domain = "http://%s.%s.com" % (sub, parent)
                for resp in self.iter_responses('/test_regex_list',
                                                headers={'origin': domain}):
                    self.assertEqual(domain, resp.headers.get(ACL_ORIGIN))

    def test_regex_mixed_list(self):
        '''
            Tests  the corner case occurs when the send_always setting is True
            and no Origin header in the request, it is not possible to match
            the regular expression(s) to determine the correct
            Access-Control-Allow-Origin header to be returned. Instead, the
            list of origins is serialized, and any strings which seem like
            regular expressions (e.g. are not a '*' and contain either '*'
            or '?') will be skipped.

            Thus, the list of returned Access-Control-Allow-Origin header
            is garaunteed to be 'null', the origin or "*", as per the w3
            http://www.w3.org/TR/cors/#access-control-allow-origin-response-header

        '''
        for sub in letters:
            domain = "http://%s.otherexample.com" % sub
            for resp in self.iter_responses('/test_regex_mixed_list',
                                            origin=domain):
                self.assertEqual(domain, resp.headers.get(ACL_ORIGIN))

        self.assertEquals("http://example.com",
            self.get('/test_regex_mixed_list', origin='http://example.com').headers.get(ACL_ORIGIN))


class AppExtensionList(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources=[r'/test_exposed', r'/test_other_exposed'],
             origins=['http://foo.com', 'http://bar.com'])

        @self.app.route('/test_unexposed')
        def unexposed():
            return 'Not exposed over CORS!'

        @self.app.route('/test_exposed')
        def exposed1():
            return 'Welcome!'

        @self.app.route('/test_other_exposed')
        def exposed2():
            return 'Welcome!'

    def test_exposed(self):
        for resp in self.iter_responses('/test_exposed', origin='http://foo.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN),'http://foo.com')

    def test_other_exposed(self):
        for resp in self.iter_responses('/test_other_exposed', origin='http://bar.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://bar.com')

    def test_unexposed(self):
        for resp in self.iter_responses('/test_unexposed', origin='http://foo.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)


class AppExtensionString(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources=r'/api/*',
             headers='Content-Type',
             expose_headers='X-Total-Count',
             origins='http://bar.com')

        @self.app.route('/api/v1/foo')
        def exposed1():
            return jsonify(success=True)

        @self.app.route('/api/v1/bar')
        def exposed2():
            return jsonify(success=True)

        @self.app.route('/api/v1/special')
        @cross_origin(origins='http://foo.com')
        def overridden():
            return jsonify(special=True)

        @self.app.route('/')
        def index():
            return 'Welcome'

    def test_exposed(self):
        for path in '/api/v1/foo', '/api/v1/bar':
            for resp in self.iter_responses(path, origin='http://bar.com'):
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://bar.com')
                self.assertEqual(resp.headers.get(ACL_EXPOSE_HEADERS),
                                 'X-Total-Count')
            for resp in self.iter_responses(path, origin='http://foo.com'):
                self.assertEqual(resp.status_code, 200)
                self.assertFalse(ACL_ORIGIN in resp.headers)
                self.assertFalse(ACL_EXPOSE_HEADERS in resp.headers)

    def test_unexposed(self):
        for resp in self.iter_responses('/', origin='http://bar.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)
            self.assertFalse(ACL_EXPOSE_HEADERS in resp.headers)

    def test_override(self):
        for resp in self.iter_responses('/api/v1/special', origin='http://foo.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://foo.com')

            self.assertFalse(ACL_EXPOSE_HEADERS in resp.headers)

        for resp in self.iter_responses('/api/v1/special', origin='http://bar.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)
            self.assertFalse(ACL_EXPOSE_HEADERS in resp.headers)


class AppExtensionError(FlaskCorsTestCase):
    def test_value_error(self):
        try:
            app = Flask(__name__)
            CORS(app, resources=5)
            self.assertTrue(False, "Should've raised a value error")
        except ValueError:
            pass


class AppExtensionDefault(FlaskCorsTestCase):
    def test_default(self):
        '''
            By default match all.
        '''

        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/')
        def index():
            return 'Welcome'

        for resp in self.iter_responses('/', origin='http://foo.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(ACL_ORIGIN in resp.headers)


class AppExtensionExampleApp(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={
            r'/api/*': {'origins': ['http://blah.com', 'http://foo.bar']}
        })

        @self.app.route('/')
        def index():
            return ''

        @self.app.route('/api/foo')
        def test_wildcard():
            return ''

        @self.app.route('/api/')
        def test_exact_match():
            return ''

    def test_index(self):
        '''
            If regex does not match, do not set CORS
        '''
        for resp in self.iter_responses('/', origin='http://foo.bar'):
            self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_wildcard(self):
        '''
            Match anything matching the path /api/* with an origin
            of 'http://blah.com' or 'http://foo.bar'
        '''
        for origin in ['http://foo.bar', 'http://blah.com']:
            for resp in self.iter_responses('/api/foo', origin=origin):
                self.assertTrue(ACL_ORIGIN in resp.headers)
                self.assertEqual(origin, resp.headers.get(ACL_ORIGIN))

    def test_exact_match(self):
        '''
            Match anything matching the path /api/* with an origin
            of 'http://blah.com' or 'http://foo.bar'
        '''
        for origin in ['http://foo.bar', 'http://blah.com']:
            for resp in self.iter_responses('/api/', origin=origin):
                self.assertTrue(ACL_ORIGIN in resp.headers)
                self.assertEqual(origin, resp.headers.get(ACL_ORIGIN))


class AppExtensionCompiledRegexp(FlaskCorsTestCase):
    def test_compiled_regex(self):
        '''
            Ensure we do not error if the user sepcifies an bad regular
            expression.
        '''
        import re
        self.app = Flask(__name__)
        CORS(self.app, resources=re.compile('/api/.*'))

        @self.app.route('/')
        def index():
            return 'Welcome'

        @self.app.route('/api/v1')
        def example():
            return 'Welcome'

        for resp in self.iter_responses('/'):
            self.assertFalse(ACL_ORIGIN in resp.headers)

        for resp in self.iter_responses('/api/v1', origin='http://foo.com'):
            self.assertTrue(ACL_ORIGIN in resp.headers)


class AppExtensionBadRegexp(FlaskCorsTestCase):
    def test_value_error(self):
        '''
            Ensure we do not error if the user sepcifies an bad regular
            expression.
        '''

        self.app = Flask(__name__)
        CORS(self.app, resources="[")

        @self.app.route('/')
        def index():
            return 'Welcome'

        for resp in self.iter_responses('/'):
            self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
