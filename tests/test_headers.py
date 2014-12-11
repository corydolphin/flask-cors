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


class HeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_override')
        @cross_origin(headers=["Foo", "Bar"])
        def test_override():
            return 'Welcome!'

    def test_default(self):
        for resp in self.iter_responses('/test_default'):
            self.assertTrue(resp.headers.get(ACL_HEADERS) is None,
                            "Default should have no allowed headers")

    def test_override(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        for resp in self.iter_responses('/test_override'):
            self.assertEqual(resp.headers.get(ACL_HEADERS), 'Bar, Foo')


class AppConfigHeadersTestCase(AppConfigTest, HeadersTestCase):
    def __init__(self, *args, **kwargs):
        super(AppConfigHeadersTestCase, self).__init__(*args, **kwargs)

    def test_default(self):
        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'
        super(AppConfigHeadersTestCase, self).test_default()

    def test_override(self):
        self.app.config['CORS_HEADERS'] = ['Foo', 'Bar']

        @self.app.route('/test_override')
        @cross_origin()
        def test_list():
            return 'Welcome!'

        super(AppConfigHeadersTestCase, self).test_override()



if __name__ == "__main__":
    unittest.main()
