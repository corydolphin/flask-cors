# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from tests.base_test import FlaskCorsTestCase, AppConfigTest
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class ExposeHeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_list')
        @cross_origin(expose_headers=["Foo", "Bar"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(expose_headers="Foo")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(expose_headers=set(["Foo", "Bar"]))
        def test_set():
            return 'Welcome!'

    def test_default(self):
        with self.app.test_client() as c:
            resp =  c.get('/test_default')
            self.assertTrue(resp.headers.get(ACL_EXPOSE_HEADERS) is None,
                            "Default should have no allowed headers")

    def test_list_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            resp =  c.get('/test_list')
            self.assertEqual(resp.headers.get(ACL_EXPOSE_HEADERS), 'Bar, Foo')

    def test_string_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            resp =  c.get('/test_string')
            self.assertEqual(resp.headers.get(ACL_EXPOSE_HEADERS), 'Foo')

    def test_set_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            resp =  c.get('/test_set')
            self.assertEqual(resp.headers.get(ACL_EXPOSE_HEADERS), 'Bar, Foo')


class AppConfigExposeHeadersTestCase(AppConfigTest, ExposeHeadersTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigExposeHeadersTestCase, self).__init__(*args, **kwargs)

    def test_default(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'
        super(AppConfigExposeHeadersTestCase, self).test_default()

    def test_list_serialized(self):
        self.app = Flask(__name__)
        self.app.config['CORS_EXPOSE_HEADERS'] = ["Foo", "Bar"]

        @self.app.route('/test_list')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigExposeHeadersTestCase, self).test_list_serialized()

    def test_string_serialized(self):
        self.app = Flask(__name__)
        self.app.config['CORS_EXPOSE_HEADERS'] = "Foo"

        @self.app.route('/test_string')
        @cross_origin()
        def test_string():
            return 'Welcome!'

        super(AppConfigExposeHeadersTestCase, self).test_string_serialized()

    def test_set_serialized(self):
        self.app = Flask(__name__)
        self.app.config['CORS_EXPOSE_HEADERS'] = set(["Foo", "Bar"])

        @self.app.route('/test_set')
        @cross_origin()
        def test_string():
            return 'Welcome!'
        super(AppConfigExposeHeadersTestCase, self).test_set_serialized()


if __name__ == "__main__":
    unittest.main()
