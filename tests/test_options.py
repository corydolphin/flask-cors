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


class OptionsTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        @self.app.route('/test_no_options_and_not_auto')
        @cross_origin(automatic_options=False)
        def test_no_options_and_not_auto():
            return 'Welcome!'

        @self.app.route('/test_options_and_not_auto', methods=['OPTIONS'])
        @cross_origin(automatic_options=False)
        def test_options_and_not_auto():
            return 'Welcome!'

    def test_defaults(self):
        '''
            The default behavior should automatically provide OPTIONS
            and return CORS headers.
        '''
        resp = self.options('/test_default')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)

        headers = {'Origin': 'http://foo.bar.com/'}
        resp = self.options('/test_default', headers=headers)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)
        self.assertEqual(resp.headers.get(ACL_ORIGIN), '*')

    def test_no_options_and_not_auto(self):
        '''
            If automatic_options is False, and the view func does not provide
            OPTIONS, then Flask's default handling will occur, and no CORS
            headers will be returned.
        '''
        resp = self.options('/test_no_options_and_not_auto')
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(ACL_ORIGIN in resp.headers)

        headers = {'Origin': 'http://foo.bar.com/'}
        resp = self.options('/test_no_options_and_not_auto', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_options_and_not_auto(self):
        '''
            If OPTIONS is in methods, and automatic_options is False,
            the view function must return a response.
        '''
        resp = self.options('/test_options_and_not_auto')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(ACL_ORIGIN in resp.headers)
        self.assertEqual(resp.data.decode("utf-8"), u"Welcome!")

        headers = {'Origin': 'http://foo.bar.com/'}
        resp = self.options('/test_options_and_not_auto', headers=headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get(ACL_ORIGIN), '*')
        self.assertEqual(resp.data.decode("utf-8"), u"Welcome!")


class AppOptionsTestCase(AppConfigTest, OptionsTestCase):
    def __init__(self, *args, **kwargs):
        super(AppOptionsTestCase, self).__init__(*args, **kwargs)

    def test_defaults(self):
        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Welcome!'

        super(AppOptionsTestCase, self).test_defaults()

    def test_no_options_and_not_auto(self):
        @self.app.route('/test_no_options_and_not_auto')
        @cross_origin(automatic_options=False)
        def test_no_options_and_not_auto():
            return 'Welcome!'
        super(AppOptionsTestCase, self).test_no_options_and_not_auto()

    def test_options_and_not_auto(self):
        self.app.config['CORS_AUTOMATIC_OPTIONS'] = False

        @self.app.route('/test_options_and_not_auto', methods=['OPTIONS'])
        @cross_origin()
        def test_options_and_not_auto():
            return 'Welcome!'
        super(AppOptionsTestCase, self).test_options_and_not_auto()


if __name__ == "__main__":
    unittest.main()
