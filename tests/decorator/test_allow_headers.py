# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from ..base_test import FlaskCorsTestCase
from flask import Flask

from flask_cors import *
from flask_cors.core import *

class AllowHeadersTestCaseIntegration(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_allow_headers')
        @cross_origin(allow_headers=['X-Example-Header-B',
                                     'X-Example-Header-A'])
        def test_allow_headers():
            return 'Welcome!'

        @self.app.route('/test_allow_headers_regex')
        @cross_origin(allow_headers=[r'X-COMPANY-.*'])
        def test_allow_headers_regex():
            return 'Welcome!'

    def test_default(self):
        for resp in self.iter_responses('/test_default'):
            self.assertTrue(resp.headers.get(ACL_ALLOW_HEADERS) is None,
                            "Default should have no allowed headers")

    def test_allow_headers_no_request_headers(self):
        '''
        No ACL_REQUEST_HEADERS sent, ACL_ALLOW_HEADERS should be empty
        '''
        resp = self.preflight('/test_allow_headers', origin='www.example.com')
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS), None)

    def test_allow_headers_with_request_headers(self):
        '''
            If there is an Access-Control-Request-Method header in the request
            and Access-Control-Request-Method is allowed for cross origin
            requests and request method is OPTIONS, and every element in the
            Access-Control-Request-Headers is an allowed header, the
            Access-Control-Allow-Headers header should be echoed back.
        '''
        resp = self.preflight('/test_allow_headers',
                              origin='www.example.com',
                              cors_request_headers=['X-Example-Header-A'])
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS),
                         'X-Example-Header-A')

    def test_allow_headers_with_unmatched_request_headers(self):
        '''
            If every element in the Access-Control-Request-Headers is not an
            allowed header, then the matching headers should be returned.
        '''
        resp = self.preflight('/test_allow_headers',
                              origin='www.example.com',
                              cors_request_headers=['X-Not-Found-Header'])
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS), None)

        resp = self.preflight('/test_allow_headers',
                              origin='www.example.com',
                              cors_request_headers=['X-Example-Header-A',
                                                    'X-Not-Found-Header'])
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS),
                         'X-Example-Header-A')

    def test_allow_headers_regex(self):
        '''
            If every element in the Access-Control-Request-Headers is not an
            allowed header, then the matching headers should be returned.
        '''
        resp = self.preflight('/test_allow_headers_regex',
                              origin='www.example.com',
                              cors_request_headers=['X-COMPANY-FOO'])
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS), 'X-COMPANY-FOO')

        resp = self.preflight('/test_allow_headers_regex',
                              origin='www.example.com',
                              cors_request_headers=['X-Not-Found-Header'])
        self.assertEqual(resp.headers.get(ACL_ALLOW_HEADERS), None)


if __name__ == "__main__":
    unittest.main()
