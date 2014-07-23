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
from tests.base_test import FlaskCorsTestCase
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
        ''' By default, Access-Control-Allow-Methods should only be returned
            if the client makes an OPTIONS request.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                self.assertFalse(ACL_MAX_AGE in verb('/defaults').headers)

    def test_string(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                self.assertEqual(
                    verb('/test_string').headers.get(ACL_MAX_AGE),
                    '600'
                )

    def test_time_delta(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                self.assertEqual(
                    verb('/test_time_delta').headers.get(ACL_MAX_AGE),
                    '600'
                )


if __name__ == "__main__":
    unittest.main()
