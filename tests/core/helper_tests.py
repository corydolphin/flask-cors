# -*- coding: utf-8 -*-
"""
    Tests for helper and utility methods
    TODO: move integration tests (e.g. all that test a full request cycle)
    into smaller, broken-up unit tests to simplify testing.
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2016 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask_cors.core import *


class InternalsTestCase(unittest.TestCase):
    def test_try_match(self):
        self.assertFalse(try_match('www.com/foo', 'www.com/fo'))
        self.assertTrue(try_match('www.com/foo', 'www.com/fo*'))

    def test_flexible_str_str(self):
        self.assertEquals(flexible_str('Bar, Foo, Qux'), 'Bar, Foo, Qux')

    def test_flexible_str_set(self):
        self.assertEquals(flexible_str(set(['Foo', 'Bar', 'Qux'])),
                          'Bar, Foo, Qux')

    def test_serialize_options(self):
        try:
            serialize_options({
                'origins': r'*',
                'allow_headers': True,
                'supports_credentials': True,
                'send_wildcard': True
            })
            self.assertFalse(True, "A Value Error should have been raised.")
        except ValueError:
            pass

    def test_get_allow_headers_empty(self):
        options = serialize_options({'allow_headers': r'*'})

        self.assertEquals(get_allow_headers(options, ''), None)
        self.assertEquals(get_allow_headers(options, None), None)

    def test_get_allow_headers_matching(self):
        options = serialize_options({'allow_headers': r'*'})

        self.assertEquals(get_allow_headers(options, 'X-FOO'), 'X-FOO')
        self.assertEquals(
            get_allow_headers(options, 'X-Foo, X-Bar'),
            'X-Bar, X-Foo'
        )

    def test_get_allow_headers_matching_none(self):
        options = serialize_options({'allow_headers': r'X-FLASK-.*'})

        self.assertEquals(get_allow_headers(options, 'X-FLASK-CORS'),
                          'X-FLASK-CORS')
        self.assertEquals(
            get_allow_headers(options, 'X-NOT-FLASK-CORS'),
            ''
        )

    def test_parse_resources_sorted(self):
        resources = parse_resources({
            '/foo': {'origins': 'http://foo.com'},
            re.compile(r'/.*'): {
                'origins': 'http://some-domain.com'
            },
            re.compile(r'/api/v1/.*'): {
                'origins': 'http://specific-domain.com'
            }
        })

        self.assertEqual(
            [r[0] for r in resources],
            [re.compile(r'/api/v1/.*'), '/foo', re.compile(r'/.*')]
        )

    def test_probably_regex(self):
        self.assertTrue(probably_regex("http://*.example.com"))
        self.assertTrue(probably_regex("*"))
        self.assertFalse(probably_regex("http://example.com"))
        self.assertTrue(probably_regex("http://[\w].example.com"))
        self.assertTrue(probably_regex("http://\w+.example.com"))
