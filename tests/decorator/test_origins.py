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
import re
from flask_cors import *
from flask_cors.core import *

letters = 'abcdefghijklmnopqrstuvwxyz'  # string.letters is not PY3 compatible


class OriginsTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

        @self.app.route('/test_send_wildcard_with_origin')
        @cross_origin(send_wildcard=True)
        def send_wildcard():
            return 'Welcome!'

        @self.app.route('/test_list')
        @cross_origin(origins=["http://foo.com", "http://bar.com"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(origins="http://foo.com")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(origins=set(["http://foo.com", "http://bar.com"]))
        def test_set():
            return 'Welcome!'

        @self.app.route('/test_subdomain_regex')
        @cross_origin(origins=r"http?://\w*\.?example\.com:?\d*/?.*")
        def _test_subdomain_regex():
            return ''

        @self.app.route('/test_compiled_subdomain_regex')
        @cross_origin(origins=re.compile(r"http?://\w*\.?example\.com:?\d*/?.*"))
        def _test_compiled_subdomain_regex():
            return ''

        @self.app.route('/test_regex_list')
        @cross_origin(origins=[r".*.example.com", r".*.otherexample.com"])
        def _test_regex_list():
            return ''

        @self.app.route('/test_regex_mixed_list')
        @cross_origin(origins=["http://example.com", r".*.otherexample.com"])
        def _test_regex_mixed_list():
            return ''

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


class AppConfigOriginsTestCase(AppConfigTest, OriginsTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigOriginsTestCase, self).__init__(*args, **kwargs)

    def test_defaults_no_origin(self):
        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_defaults_no_origin()

    def test_defaults_with_origin(self):
        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'
        super(AppConfigOriginsTestCase, self).test_defaults_with_origin()

    def test_send_wildcard_with_origin(self):
        @self.app.route('/test_send_wildcard_with_origin')
        @cross_origin(send_wildcard=True)
        def send_wildcard():
            return 'Welcome!'
        super(AppConfigOriginsTestCase, self).test_send_wildcard_with_origin()

    def test_list_serialized(self):
        self.app.config['CORS_ORIGINS'] = ["http://foo.com", "http://bar.com"]

        @self.app.route('/test_list')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_list_serialized()

    def test_string_serialized(self):
        self.app.config['CORS_ORIGINS'] = "http://foo.com"

        @self.app.route('/test_string')
        @cross_origin()
        def test_string():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_string_serialized()

    def test_set_serialized(self):
        self.app.config['CORS_ORIGINS'] = set(["http://foo.com",
                                               "http://bar.com"])

        @self.app.route('/test_set')
        @cross_origin()
        def test_set():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_set_serialized()

    def test_not_matching_origins(self):
        self.app.config['CORS_ORIGINS'] = ["http://foo.com", "http://bar.com"]

        @self.app.route('/test_list')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_not_matching_origins()

    def test_regex_list(self):
        @self.app.route('/test_regex_list')
        @cross_origin()
        def _test_regex_list():
            return 'Welcome!'

        self.app.config['CORS_ORIGINS'] = [r".*.example.com",
                                           r".*.otherexample.com"]
        super(AppConfigOriginsTestCase, self).test_regex_list()

    def test_subdomain_regex(self):
        self.app.config['CORS_ORIGINS'] = r"http?://\w*\.?example\.com:?\d*/?.*"

        @self.app.route('/test_subdomain_regex')
        @cross_origin()
        def _test_subdomain_regex():
            return ''

        super(AppConfigOriginsTestCase, self).test_subdomain_regex()

    def test_compiled_subdomain_regex(self):
        self.app.config['CORS_ORIGINS'] = r"http?://\w*\.?example\.com:?\d*/?.*"

        @self.app.route('/test_compiled_subdomain_regex')
        @cross_origin()
        def _test_compiled_subdomain_regex():
            return ''

        super(AppConfigOriginsTestCase, self).test_compiled_subdomain_regex()

    def test_regex_mixed_list(self):
        self.app.config['CORS_ORIGINS'] = ["http://example.com",
                                           r".*.otherexample.com"]

        @self.app.route('/test_regex_mixed_list')
        @cross_origin()
        def _test_regex_mixed_list():
            return ''

        super(AppConfigOriginsTestCase, self).test_regex_mixed_list()



if __name__ == "__main__":
    unittest.main()
