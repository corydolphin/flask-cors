# -*- coding: utf-8 -*-

from ..base_test import FlaskCorsTestCase
from flask import Flask

from flask_cors import *
from flask_cors.core import *


class SupportsCredentialsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_allow_private_network_access_supported')
        @cross_origin(allow_private_network=True)
        def test_private_network_supported():
            return 'Private network!'

        @self.app.route('/test_allow_private_network_access_unsupported')
        @cross_origin(allow_private_network=False)
        def test_credentials_unsupported():
            return 'Private network!'

        @self.app.route('/test_default')
        @cross_origin()
        def test_default():
            return 'Open!'

    def test_credentials_supported(self):
        """ The specified route should return the
            Access-Control-Allow-Credentials header.
        """
        resp = self.get('/test_allow_private_network_access_supported', origin='www.example.com', headers={ACL_REQUEST_HEADER_PRIVATE_NETWORK:'true'})
        self.assertEqual(resp.headers.get(ACL_RESPONSE_PRIVATE_NETWORK), 'true')

    def test_default(self):
        """ The default behavior should be to allow private network access.
        """
        resp = self.get('/test_default', origin='www.example.com', headers={ACL_REQUEST_HEADER_PRIVATE_NETWORK:'true'})
        self.assertTrue(ACL_RESPONSE_PRIVATE_NETWORK in resp.headers)

        resp = self.get('/test_default')
        self.assertFalse(ACL_RESPONSE_PRIVATE_NETWORK in resp.headers)

    def test_credentials_unsupported(self):
        """ If private network access is disabled, the header should never be sent."""
        resp = self.get('/test_allow_private_network_access_unsupported', origin='www.example.com')
        self.assertFalse(ACL_RESPONSE_PRIVATE_NETWORK in resp.headers)

        resp = self.get('/test_allow_private_network_access_unsupported', origin='www.example.com', headers={ACL_REQUEST_HEADER_PRIVATE_NETWORK:'true'})
        self.assertEqual(resp.headers.get(ACL_RESPONSE_PRIVATE_NETWORK), 'false')


if __name__ == "__main__":
    unittest.main()
