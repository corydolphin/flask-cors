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
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class OriginsTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

        @self.app.route('/test_list')
        @cross_origin(origins=["Foo", "Bar"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(origins="Foo")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(origins=set(["Foo", "Bar"]))
        def test_set():
            return 'Welcome!'

    def test_wildcard_defaults_no_origin(self):
        ''' If there is no Origin header in the request, the
            Access-Control-Allow-Origin header should not be included,
            according to the w3 spec.
        '''
        for resp in self.iter_responses('/'):
            self.assertEqual(resp.headers.get(ACL_ORIGIN), '*')

    def test_wildcard_defaults_origin(self):
        ''' If there is no Origin header in the request, the
            Access-Control-Allow-Origin header should be included, if and only
            if the always_send parameter is `True`, which is the default value.
        '''
        example_origin = 'http://example.com'
        headers = {'Origin': example_origin}
        for resp in self.iter_responses('/', headers=headers):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), '*')

    def test_list_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed.
        '''
        with self.app.test_client() as c:
            resp =  c.get('/test_list')
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'Bar, Foo')

    def test_string_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            resp =  c.get('/test_string')
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'Foo')

    def test_set_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            resp =  c.get('/test_set')

            allowed = resp.headers.get(ACL_ORIGIN)
            # Order is not garaunteed
            self.assertEqual(allowed, 'Bar, Foo')


class AppConfigOriginsTestCase(AppConfigTest, OriginsTestCase):
    def __init__(self, *args, **kwargs):
        super(OriginsTestCase, self).__init__(*args, **kwargs)

    def test_wildcard_defaults_no_origin(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_wildcard_defaults_no_origin()

    def test_wildcard_defaults_origin(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'
        super(AppConfigOriginsTestCase, self).test_wildcard_defaults_origin()

    def test_list_serialized(self):
        self.app = Flask(__name__)
        self.app.config['CORS_ORIGINS'] = ["Foo", "Bar"]

        @self.app.route('/test_list')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_list_serialized()

    def test_string_serialized(self):
        self.app = Flask(__name__)
        self.app.config['CORS_ORIGINS'] = "Foo"

        @self.app.route('/test_string')
        @cross_origin()
        def test_string():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_string_serialized()

    def test_set_serialized(self):
        self.app = Flask(__name__)
        self.app.config['CORS_ORIGINS'] = set(["Foo", "Bar"])

        @self.app.route('/test_set')
        @cross_origin()
        def test_set():
            return 'Welcome!'

        super(AppConfigOriginsTestCase, self).test_set_serialized()


if __name__ == "__main__":
    unittest.main()
