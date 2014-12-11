# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
from datetime import timedelta
import sys
from tests.base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class MaxAgeTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return 'Should only return headers on OPTIONS'

        @self.app.route('/test_string')
        @cross_origin(max_age=600)
        def test_string():
            return 'Open!'

        @self.app.route('/test_time_delta')
        @cross_origin(max_age=timedelta(minutes=10))
        def test_time_delta():
            return 'Open!'

    def test_defaults(self):
        ''' By default, no max-age headers should be returned
        '''
        for resp in self.iter_responses('/defaults'):
            self.assertFalse(ACL_MAX_AGE in resp.headers)

    def test_string(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        resp = self.preflight('/test_string')
        self.assertEqual(resp.headers.get(ACL_MAX_AGE), '600')

    def test_time_delta(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        # timedelta.total_seconds is not available in older versions of Python
        if sys.version_info < (2, 7):
            return

        resp = self.preflight('/test_time_delta')
        self.assertEqual(resp.headers.get(ACL_MAX_AGE), '600')


class AppConfigMaxAgeTestCase(AppConfigTest, MaxAgeTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigMaxAgeTestCase, self).__init__(*args, **kwargs)

    def test_defaults(self):
        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return 'Should only return headers on OPTIONS'

        super(AppConfigMaxAgeTestCase, self).test_defaults()

    def test_string(self):
        self.app.config['CORS_MAX_AGE'] = 600

        @self.app.route('/test_string')
        @cross_origin()
        def test_string():
            return 'Open!'

        super(AppConfigMaxAgeTestCase, self).test_string()

    def test_time_delta(self):
        self.app.config['CORS_MAX_AGE'] = timedelta(minutes=10)

        @self.app.route('/test_time_delta')
        @cross_origin()
        def test_time_delta():
            return 'Open!'

        super(AppConfigMaxAgeTestCase, self).test_time_delta()

    def test_override(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        # timedelta.total_seconds is not available in older versions of Python
        self.app.config['CORS_MAX_AGE'] = 600

        @self.app.route('/test_override')
        @cross_origin(max_age=900)
        def test_override():
            return 'Welcome!'

        resp = self.preflight('/test_override')
        self.assertEqual(resp.headers.get(ACL_MAX_AGE), '900')


if __name__ == "__main__":
    unittest.main()
