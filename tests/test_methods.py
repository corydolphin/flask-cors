# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

from tests.base_test import FlaskCorsTestCase
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class MethodsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/defaults')
        @cross_origin()
        def defaults():
            return 'Should only return headers on OPTIONS'

        @self.app.route('/get')
        @cross_origin(methods=['GET'])
        def test_open():
            return 'Open!'

    def test_defaults(self):
        ''' By default, Access-Control-Allow-Methods should only be returned
            if the client makes an OPTIONS request.
        '''
        with self.app.test_client() as c:
            self.assertFalse(ACL_METHODS in c.get('/defaults').headers)
            self.assertFalse(ACL_METHODS in c.head('/defaults').headers)
            self.assertTrue(ACL_METHODS in c.options('/defaults').headers)

    def test_methods_defined(self):
        ''' If the methods parameter is defined, always return the allowed
            methods defined by the user.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                self.assertTrue(ACL_METHODS in verb('/get').headers)
                self.assertTrue('GET' in verb('/get').headers[ACL_METHODS])


if __name__ == "__main__":
    unittest.main()
