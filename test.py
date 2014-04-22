# -*- coding: utf-8 -*-
"""
    test
    ~~~~

    Flask-Cors tests module
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask import Flask

try:
    # support local usage without installed package
    from flask_cors import cross_origin
except:
    # this is how you would normally import
    from flask.ext.cors import cross_origin

AccessControlAllowOrigin = 'Access-Control-Allow-Origin'


class FlaskCorsTestCase(unittest.TestCase):
    def iter_verbs(self, c):
        ''' A simple helper method to iterate through a range of
            HTTP Verbs and return the test_client bound instance,
            keeping writing our tests as DRY as possible.
        '''
        for verb in ['get', 'head', 'options']:
            yield getattr(c, verb)


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
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertEqual(result.headers.get(AccessControlAllowOrigin),
                                 '*')

    def test_app_configured_origins(self):
        ''' If the application contains a list of origins in the
            `CORS_ORIGINS` config value, then origins should default to them
            instead of '*'
        '''
        app = Flask(__name__)
        app.config['CORS_ORIGINS'] = ['Foo', 'Bar']

        @app.route('/')
        @cross_origin(methods=['GET', 'OPTIONS', 'HEAD', 'PUT', 'POST'])
        def wildcard():
            return 'Welcome!'

        with app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertEqual(
                    result.headers.get(AccessControlAllowOrigin),
                    'Foo, Bar'
                )

    def test_wildcard_defaults_origin(self):
        ''' If there is no Origin header in the request, the
            Access-Control-Allow-Origin header should be included, if and only
            if the always_send parameter is `True`, which is the default value.
        '''
        example_origin = 'http://example.com'
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/', headers={'Origin': example_origin})
                self.assertEqual(result.status_code, 200)
                self.assertEqual(
                    result.headers.get(AccessControlAllowOrigin),
                    '*'
                )

    def test_list_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_list')
            self.assertEqual(
                result.headers.get(AccessControlAllowOrigin),
                'Foo, Bar'
            )

    def test_string_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_string')
            self.assertEqual(
                result.headers.get(AccessControlAllowOrigin),
                'Foo'
            )

    def test_set_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_set')

            allowed = result.headers.get(AccessControlAllowOrigin)
            # Order is not garaunteed
            self.assertTrue(allowed == 'Foo, Bar' or allowed == 'Bar, Foo')


class OriginsW3TestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin(origins='*', send_wildcard=False, always_send=False)
        def allowOrigins():
            ''' This sets up flask-cors to echo the request's `Origin` header,
                only if it is actually set. This behavior is most similar to
                the actual W3 specification, http://www.w3.org/TR/cors/ but
                is not the default because it is more common to use the
                wildcard configuration in order to support CDN caching.
            '''
            return 'Welcome!'

    def test_wildcard_origin_header(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        example_origin = 'http://example.com'
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/', headers={'Origin': example_origin})
                self.assertEqual(
                    result.headers.get(AccessControlAllowOrigin),
                    example_origin
                )

    def test_wildcard_no_origin_header(self):
        ''' If there is no Origin header in the request, the
            Access-Control-Allow-Origin header should not be included.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertTrue(AccessControlAllowOrigin not in result.headers)


class HeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_list')
        @cross_origin(headers=["Foo", "Bar"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(headers="Foo")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(headers=set(["Foo", "Bar"]))
        def test_set():
            return 'Welcome!'

    def test_list_serialized(self):
        ''' If there is an Origin header in the request,
            the Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_list')
            self.assertEqual(
                result.headers.get('Access-Control-Allow-Headers'),
                'Foo, Bar'
            )

    def test_string_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_string')
            self.assertEqual(
                result.headers.get('Access-Control-Allow-Headers'),
                'Foo'
            )

    def test_set_serialized(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_set')

            allowed = result.headers.get('Access-Control-Allow-Headers')
            # Order is not garaunteed for sets
            self.assertTrue(allowed in ['Foo, Bar', 'Bar, Foo'])


class SupportsCredentialsCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_credentials')
        @cross_origin(supports_credentials=True)
        def test_credentials():
            return 'Credentials!'

        @self.app.route('/test_open')
        @cross_origin()
        def test_open():
            return 'Open!'

    def test_credentialed_request(self):
        ''' The specified route should return the
            Access-Control-Allow-Credentials header.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_credentials')
            header = result.headers.get('Access-Control-Allow-Credentials')
            self.assertEquals(header, 'true')

    def test_open_request(self):
        ''' The default behavior should be to disallow credentials.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_open')
            self.assertTrue(
                'Access-Control-Allow-Credentials' not in result.headers
            )


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
        with self.app.test_client() as c:
            result = c.options('/test_default')
            self.assertEqual(result.status_code, 200)
            self.assertTrue(AccessControlAllowOrigin in result.headers)

            headers = {'Origin': 'http://foo.bar.com/'}
            result = c.options('/test_default', headers=headers)

            self.assertEqual(result.status_code, 200)
            self.assertTrue(AccessControlAllowOrigin in result.headers)
            self.assertEqual(result.headers[AccessControlAllowOrigin], '*')

    def test_no_options_and_not_auto(self):
        '''
            If automatic_options is False, and the view func does not provide
            OPTIONS, then Flask's default handling will occur, and no CORS
            headers will be returned.
        '''
        with self.app.test_client() as c:
            result = c.options('/test_no_options_and_not_auto')
            self.assertEqual(result.status_code, 200)
            self.assertFalse(AccessControlAllowOrigin in result.headers)

            headers = {'Origin': 'http://foo.bar.com/'}
            result = c.options('/test_no_options_and_not_auto',
                               headers=headers)
            self.assertEqual(result.status_code, 200)
            self.assertFalse(AccessControlAllowOrigin in result.headers)

    def test_options_and_not_auto(self):
        '''
            If OPTIONS is in methods, and automatic_options is False,
            the view function must return a response.
        '''
        with self.app.test_client() as c:
            result = c.options('/test_options_and_not_auto')
            self.assertEqual(result.status_code, 200)
            self.assertTrue(AccessControlAllowOrigin in result.headers)
            self.assertEqual(result.data.decode("utf-8"), u"Welcome!")

            headers = {'Origin': 'http://foo.bar.com/'}
            result = c.options('/test_options_and_not_auto', headers=headers)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.headers[AccessControlAllowOrigin], '*')
            self.assertEqual(result.data.decode("utf-8"), u"Welcome!")

if __name__ == "__main__":
    unittest.main()
