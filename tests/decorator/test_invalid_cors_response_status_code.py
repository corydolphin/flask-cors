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
from flask import Flask
from flask_cors import *
from flask_cors.core import *


class DecoratorInvalidCorsResponseStatusCode(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/with_no_options')
        @cross_origin(origins=['http://valid.com'])
        def with_no_options():
            return 'NO OPTIONS!'

        @self.app.route('/with_client_error_status')
        @cross_origin(
            origins=['http://valid.com'],
            invalid_cors_status_code=403
        )
        def with_client_error_status():
            return 'WITH 403!'

        @self.app.route('/with_non_client_error_response')
        @cross_origin(
            origins=['http://valid.com'],
            invalid_cors_status_code=304
        )
        def with_non_client_error_response():
            return 'WITH 304!'

    def test_with_no_options(self):
        ''' If no `invalid_cors_status_code` options set,
            response code OK(200) will be returned
            when invalid CORS request.
        '''
        for index, resp in enumerate(self.iter_responses(
                '/with_no_options',
                verbs=['get', 'head', 'options'],
                origin='http://valid.com'
            )):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://valid.com')
            expected = u'NO OPTIONS!' if index == 0 else u''
            self.assertEqual(resp.data.decode('utf-8'), expected)

        for index, resp in enumerate(self.iter_responses(
                '/with_no_options',
                verbs=['get', 'head', 'options'],
                origin='http://invalid.com'
            )):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), None)
            expected = u'NO OPTIONS!' if index == 0 else u''
            self.assertEqual(resp.data.decode('utf-8'), expected)

    def test_with_client_error_status(self):
        ''' If `invalid_cors_status_code` options set as 403,
            which is Clinet Error Status Code, response code
            FORBIDDEN(403) will be returned when invalid CORS
            request.
        '''
        for index, resp in enumerate(self.iter_responses(
                '/with_client_error_status',
                verbs=['get', 'head', 'options'],
                origin='http://valid.com'
            )):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://valid.com')
            expected = u'WITH 403!' if index == 0 else u''
            self.assertEqual(resp.data.decode('utf-8'), expected)

        for resp in self.iter_responses('/with_client_error_status', origin='http://invalid.com'):
            self.assertEqual(resp.status_code, 403)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), None)
            self.assertEqual(resp.data.decode('utf-8'), u'')

    def test_with_non_client_error_status(self):
        ''' If `invalid_cors_status_code` options set as 200,
            which is not Clinet Error Status Code, response
            code OK(200) will be returned when invalid CORS
            request.
        '''
        for index, resp in enumerate(self.iter_responses(
                '/with_non_client_error_response',
                verbs=['get', 'head', 'options'],
                origin='http://valid.com'
            )):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://valid.com')
            expected = u'WITH 304!' if index == 0 else u''
            self.assertEqual(resp.data.decode('utf-8'), expected)

        for resp in self.iter_responses('/with_non_client_error_response', origin='http://invalid.com'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), None)
            self.assertEqual(resp.data.decode('utf-8'), u'')


if __name__ == "__main__":
    unittest.main()
