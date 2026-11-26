# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2016 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
import unittest

from ..base_test import FlaskCorsTestCase
from flask import Flask, abort
from flask_cors import *
from flask_cors.core import *


class DecoratorErrorResponseTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_abort_401')
        @cross_origin()
        def test_abort_401():
            abort(401)

        @self.app.route('/test_abort_403_custom_handler')
        @cross_origin()
        def test_abort_403_custom_handler():
            abort(403)

        @self.app.errorhandler(403)
        def custom_403(e):
            return 'custom forbidden', 403

    def test_abort_response_carries_cors_headers(self):
        ''' HTTPExceptions raised in a decorated view must still produce
            a response carrying the CORS headers.
        '''
        resp = self.get('/test_abort_401', origin='www.example.com')
        self.assertEqual(resp.status_code, 401)
        self.assertTrue(ACL_ORIGIN in resp.headers)

    def test_custom_error_handler_still_applies(self):
        ''' Registered error handlers must keep handling HTTPExceptions
            raised in a decorated view.
        '''
        resp = self.get('/test_abort_403_custom_handler', origin='www.example.com')
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.data, b'custom forbidden')
        self.assertTrue(ACL_ORIGIN in resp.headers)

    def test_normal_response_unchanged(self):
        ''' Undecorated routes are unaffected.
        '''
        resp = self.get('/route_does_not_exist', origin='www.example.com')
        self.assertEqual(resp.status_code, 404)
        self.assertFalse(ACL_ORIGIN in resp.headers)


if __name__ == "__main__":
    unittest.main()
