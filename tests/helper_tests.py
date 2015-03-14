# -*- coding: utf-8 -*-
"""
    Tests for helper and utility methods
    TODO: move integration tests (e.g. all that test a full request cycle)
    into smaller, broken-up unit tests to simplify testing.
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask_cors.core import *


class InternalsTestCase(unittest.TestCase):
    def testtry_match(self):
        self.assertTrue(try_match('www.com/foo+', 'www.com/foo+'))

    def testflexible_str_str(self):
        self.assertEquals(flexible_str('Bar, Foo, Qux'), 'Bar, Foo, Qux')

    def testflexible_str_set(self):
        self.assertEquals(flexible_str(set(['Foo', 'Bar', 'Qux'])),
                          'Bar, Foo, Qux')

    def testserialize_options(self):
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
