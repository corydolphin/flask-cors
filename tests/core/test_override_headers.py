# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

from ..base_test import FlaskCorsTestCase
from flask import Flask, Response

from flask_cors import *
from flask_cors.core import *

class ResponseHeadersOverrideTestCaseIntegration(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/')
        def index():
            response = Response(headers={"custom": "dictionary"})
            return 'Welcome'

    def test_override_headers(self):
        '''
            Ensure we work even if response.headers is set to something other than a MultiDict.
        '''
        for resp in self.iter_responses('/'):
            self.assertTrue(ACL_ORIGIN in resp.headers)

if __name__ == "__main__":
    unittest.main()
