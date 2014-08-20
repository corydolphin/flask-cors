# -*- coding: utf-8 -*-
"""
    test
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
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *


class FlaskCorsTestCase(unittest.TestCase):
    def shortDescription(self):
        """
        Get's the one liner description to be displayed.
        Source:
        http://erikzaadi.com/2012/09/13/inheritance-within-python-unit-tests/
        """
        doc = self._testMethodDoc
        doc = doc and doc.split("\n")[0].strip() or ""
        return "%s : %s" % (self.__class__.__name__, doc)

    def iter_verbs(self, c):
        ''' A simple helper method to iterate through a range of
            HTTP Verbs and return the test_client bound instance,
            keeping writing our tests as DRY as possible.
        '''
        for verb in ['get', 'head', 'options']:
            yield getattr(c, verb)

    def iter_responses(self, path, verbs=['get', 'head', 'options'], **kwargs):
        with self.app.test_client() as c:
            for verb in verbs:
                yield getattr(c, verb.lower())(path, **kwargs)

    def _request(self, verb, *args, **kwargs):
        with self.app.test_client() as c:
            return getattr(c, verb)(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request('get', *args, **kwargs)

    def head(self, *args, **kwargs):
        return self._request('head', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self._request('options', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request('put', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._request('patch', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request('delete', *args, **kwargs)


class AppConfigTest(object):
    def setUp(self):
        self.app = Flask(self.__class__.__name__)

    def tearDown(self):
        self.app = None
