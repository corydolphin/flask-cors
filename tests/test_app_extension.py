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
from tests.test_origins import OriginsTestCase
from tests.test_options import OptionsTestCase
from flask import Flask, jsonify

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class AppExtensionRegexp(AppConfigTest, OriginsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={
            r'/': {},
            r'/test_list': {'origins': ["http://foo.com", "http://bar.com"]},
            r'/test_string': {'origins': 'http://foo.com'},
            r'/test_set': {
                'origins': set(["http://foo.com", "http://bar.com"])
            },
            r'/test_subdomain_regex': {
                'origins': r"http?://\w*\.?example\.com:?\d*/?.*"
            },
            r'/test_regex_list': {
                'origins': [r".*.example.com", r".*.otherexample.com"]
            },
            r'/test_regex_mixed_list': {
                'origins': ["http://example.com", r".*.otherexample.com"]
            }
        })

        @self.app.route('/')
        def wildcard():
            return 'Welcome!'

        @self.app.route('/test_list')
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        def test_set():
            return 'Welcome!'


class AppExtensionList(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources=[r'/test_exposed', r'/test_other_exposed'],
             origins=['http://foo.com, http://bar.com'])

        @self.app.route('/test_unexposed')
        def unexposed():
            return 'Not exposed over CORS!'

        @self.app.route('/test_exposed')
        def exposed1():
            return 'Welcome!'

        @self.app.route('/test_other_exposed')
        def exposed2():
            return 'Welcome!'

    def test_exposed(self):
        for resp in self.iter_responses('/test_exposed'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN),
                             'http://foo.com, http://bar.com')

    def test_other_exposed(self):
        for resp in self.iter_responses('/test_other_exposed'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN),
                             'http://foo.com, http://bar.com')

    def test_unexposed(self):
        for resp in self.iter_responses('/test_unexposed'):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)


class AppExtensionString(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources=r'/api/*',
             headers='Content-Type',
             expose_headers='X-Total-Count')

        @self.app.route('/api/v1/foo')
        def exposed1():
            return jsonify(success=True)

        @self.app.route('/api/v1/bar')
        def exposed2():
            return jsonify(success=True)

        @self.app.route('/api/v1/special')
        @cross_origin(origins='http://foo.com')
        def overridden():
            return jsonify(special=True)

        @self.app.route('/')
        def index():
            return 'Welcome'

    def test_exposed(self):
        for path in '/api/v1/foo', '/api/v1/bar':
            for resp in self.iter_responses(path):
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(resp.headers.get(ACL_ORIGIN), '*')
                self.assertEqual(resp.headers.get(ACL_EXPOSE_HEADERS),
                                 'X-Total-Count')

    def test_unexposed(self):
        for resp in self.iter_responses('/'):
            self.assertEqual(resp.status_code, 200)
            self.assertFalse(ACL_ORIGIN in resp.headers)
            self.assertFalse(ACL_EXPOSE_HEADERS in resp.headers)

    def test_override(self):
        for resp in self.iter_responses('/api/v1/special'):
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.headers.get(ACL_ORIGIN), 'http://foo.com')

            self.assertFalse(ACL_EXPOSE_HEADERS in resp.headers)


class AppExtensionError(FlaskCorsTestCase):
    def test_value_error(self):
        try:
            app = Flask(__name__)
            CORS(app, resources=5)
            self.assertTrue(False, "Should've raised a value error")
        except ValueError:
            pass


class AppExtensionDefault(FlaskCorsTestCase):
    def test_default(self):
        '''
            By default match all.
        '''

        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/')
        def index():
            return 'Welcome'

        for resp in self.iter_responses('/'):
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(ACL_ORIGIN in resp.headers)


class AppExtensionExampleApp(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={
            r'/api/*': {'origins': ['http://blah.com', 'http://foo.bar']}
        })

        @self.app.route('/')
        def index():
            return ''

        @self.app.route('/api/foo')
        def test_wildcard():
            return ''

        @self.app.route('/api/')
        def test_exact_match():
            return ''

    def test_index(self):
        '''
            If regex does not match, do not set CORS
        '''
        for resp in self.iter_responses('/'):
            self.assertFalse(ACL_ORIGIN in resp.headers)

    def test_wildcard(self):
        '''
            Match anything matching the path /api/* with an origin
            of 'http://blah.com' or 'http://foo.bar'
        '''
        for origin in ['http://foo.bar', 'http://blah.com']:
            for resp in self.iter_responses('/api/foo', origin=origin):
                self.assertTrue(ACL_ORIGIN in resp.headers)
                self.assertEqual(origin, resp.headers.get(ACL_ORIGIN))

    def test_exact_match(self):
        '''
            Match anything matching the path /api/* with an origin
            of 'http://blah.com' or 'http://foo.bar'
        '''
        for origin in ['http://foo.bar', 'http://blah.com']:
            for resp in self.iter_responses('/api/', origin=origin):
                self.assertTrue(ACL_ORIGIN in resp.headers)
                self.assertEqual(origin, resp.headers.get(ACL_ORIGIN))


class AppExtensionCompiledRegexp(FlaskCorsTestCase):
    def test_compiled_regex(self):
        '''
            Ensure we do not error if the user sepcifies an bad regular
            expression.
        '''
        import re
        self.app = Flask(__name__)
        CORS(self.app, resources=re.compile('/api/.*'))

        @self.app.route('/')
        def index():
            return 'Welcome'

        @self.app.route('/api/v1')
        def example():
            return 'Welcome'

        for resp in self.iter_responses('/'):
            self.assertFalse(ACL_ORIGIN in resp.headers)

        for resp in self.iter_responses('/api/v1'):
            self.assertTrue(ACL_ORIGIN in resp.headers)


class AppExtensionBadRegexp(FlaskCorsTestCase):
    def test_value_error(self):
        '''
            Ensure we do not error if the user sepcifies an bad regular
            expression.
        '''

        self.app = Flask(__name__)
        CORS(self.app, resources="[")

        @self.app.route('/')
        def index():
            return 'Welcome'

        for resp in self.iter_responses('/'):
            self.assertEqual(resp.status_code, 200)


class AppExtensionOptionsTestCase(OptionsTestCase):
    def __init__(self, *args, **kwargs):
        super(AppExtensionOptionsTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.app = Flask(__name__)
        CORS(self.app)

    def test_defaults(self):
        @self.app.route('/test_default')
        def test_default():
            return 'Welcome!'

        super(AppExtensionOptionsTestCase, self).test_defaults()

    def test_no_options_and_not_auto(self):
        # This test isn't applicable since we the CORS App extension
        # Doesn't need to add options handling to view functions, since
        # it is called after_request, and will simply process the autogenerated
        # Flask OPTIONS response
        pass

    def test_options_and_not_auto(self):
        self.app.config['CORS_AUTOMATIC_OPTIONS'] = False

        @self.app.route('/test_options_and_not_auto', methods=['OPTIONS'])
        def test_options_and_not_auto():
            return 'Welcome!'
        super(AppExtensionOptionsTestCase, self).test_options_and_not_auto()


class AppExtensionSortedResourcesTestCase(FlaskCorsTestCase):
    def setUp(self):

        from flask_cors import _parse_resources

        self.resources = _parse_resources({
            '/foo': {'origins': 'http://foo.com'},
            re.compile(r'/.*'): {
                'origins': 'http://some-domain.com'
            },
            re.compile(r'/api/v1/.*'): {
                'origins': 'http://specific-domain.com'
            }
        })

    def test_sorted_order(self):
        def _get_pattern(p):
            try:
                return p.pattern
            except AttributeError:
                return p

        self.assertEqual(
            [_get_pattern(reg) for reg, opt in self.resources],
            [r'/api/v1/.*', '/foo', r'/.*']
        )


if __name__ == "__main__":
    unittest.main()
