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
        doc = self.id()[self.id().rfind('.')+1:]
        return "%s.%s" % (self.__class__.__name__, doc)

    def iter_verbs(self, c):
        ''' A simple helper method to iterate through a range of
            HTTP Verbs and return the test_client bound instance,
            keeping writing our tests as DRY as possible.
        '''
        for verb in ['get', 'head', 'options']:
            yield getattr(c, verb)

    def iter_responses(self, path, verbs=['get', 'head', 'options'], **kwargs):
        for verb in verbs:
            yield self._request(verb.lower(), path, **kwargs)
        # with self.app.test_client() as c:
        #     for verb in verbs:
        #         yield getattr(c, verb.lower())(path, **kwargs)

    def _request(self, verb, *args, **kwargs):
        _origin = kwargs.pop('origin', None)
        if _origin:
            kwargs['headers'] = kwargs.get('headers', {})
            kwargs['headers'].update(Origin=_origin)

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

    def preflight(self, path, method='GET', json=True):
        headers = {'Access-Control-Request-Method': method}
        if json:
            headers.update({'Content-Type':'application/json'})

        return self.options(path,headers=headers)

    def assertHasACLOrigin(self, resp, origin=None):
        if origin is None:
            self.assertTrue(ACL_ORIGIN in resp.headers)
        else:
            self.assertTrue(resp.headers.get(ACL_ORIGIN) == origin)


class AppConfigTest(object):
    def setUp(self):
        self.app = Flask(import_name=__name__)

    def tearDown(self):
        self.app = None

    def add_route(self, path):

        # Flask checks the name of the function to ensure that iew mappings
        # do not collide. We work around it by generating a new function name
        # for the path
        def function_to_rename():
            return 'STUBBED: %s' % path
        function_to_rename.__name__ = 'func_%s' % path

        self.app.route(path)(function_to_rename)

