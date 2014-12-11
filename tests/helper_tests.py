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
from flask import Flask
try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    # this is how you would normally import
    from flask.ext.cors import _try_match, _flexible_str
except:
    # support local usage without installed package
    from flask_cors import _try_match, _flexible_str

class InternalsTestCase(unittest.TestCase):
    def test_try_match(self):
        self.assertTrue(_try_match('www.com/foo+', 'www.com/foo+'))

    def test_flexible_str_str(self):
        self.assertEquals(_flexible_str('Bar, Foo, Qux'), 'Bar, Foo, Qux')

    def test_flexible_str_set(self):
        self.assertEquals(_flexible_str(set(['Foo', 'Bar', 'Qux'])),
            'Bar, Foo, Qux')

