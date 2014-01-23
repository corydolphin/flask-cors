try:
    import unittest2 as unittest
except ImportError:
    import unittest

from flask import Flask
try:
  from flask_cors import cross_origin # support local usage without installed package
except:
  from flask.ext.cors import cross_origin # this is how you would normally import

AccessControlAllowOrigin = 'Access-Control-Allow-Origin'

class FlaskCorsTestCase(unittest.TestCase):
    def iter_verbs(self,c):
        ''' A simple helper method to iterate through a range of 
            HTTP Verbs and return the test_client bound instance,
            keeping writing our tests as DRY as possible.
        '''
        for verb in ['get', 'head','options']:
            yield getattr(c,verb)

class OriginsTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin()
        def wildcard():
            return 'Welcome!'

    def test_wildcard_defaults_no_origin(self):
        ''' If there is no Origin header in the request, the Access-Control-Allow-Origin
            header should not be included, according to the w3 spec.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertEqual(result.headers.get(AccessControlAllowOrigin), '*')

    def test_wildcard_defaults_origin(self):
        ''' If there is no Origin header in the request, the Access-Control-Allow-Origin
            header should be included, if and only if the always_send parameter is
            `True`, which is the default value.
        '''
        example_origin = 'http://example.com'
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/',headers = {'Origin': example_origin})
                self.assertEqual(result.headers.get(AccessControlAllowOrigin),'*')


class OriginsW3TestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin(origins='*', send_wildcard=False, always_send=False)
        def allowOrigins():
            ''' This sets up flask-cors to echo the request's `Origin` header,
                only if it is actually set. This behavior is most similar to the
                actual W3 specification, http://www.w3.org/TR/cors/ but
                is not the default because it is more common to use the wildcard
                approach. 
            '''
            return 'Welcome!'

    def test_wildcard_origin_header(self):
        ''' If there is an Origin header in the request, the Access-Control-Allow-Origin
            header should be echoed back.
        '''
        example_origin = 'http://example.com'
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/', headers = {'Origin': example_origin})
                self.assertEqual(result.headers.get(AccessControlAllowOrigin),example_origin)

    def test_wildcard_no_origin_header(self):
        ''' If there is no Origin header in the request, the Access-Control-Allow-Origin
            header should not be included.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertTrue(AccessControlAllowOrigin not in result.headers)


class HeadersTestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/test_list')
        @cross_origin(headers=["Foo","Bar"])
        def test_list():
            return 'Welcome!'

        @self.app.route('/test_string')
        @cross_origin(headers="Foo")
        def test_string():
            return 'Welcome!'

        @self.app.route('/test_set')
        @cross_origin(headers=set(["Foo","Bar"]))
        def test_set():
            return 'Welcome!'


    def test_list_serialized(self):
        ''' If there is an Origin header in the request, the Access-Control-Allow-Origin
            header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_list')
            self.assertEqual(result.headers.get('Access-Control-Allow-Headers'),'Foo, Bar')

    def test_string_serialized(self):
        ''' If there is an Origin header in the request, the Access-Control-Allow-Origin
            header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_string')
            self.assertEqual(result.headers.get('Access-Control-Allow-Headers'),'Foo')


    def test_set_serialized(self):
        ''' If there is an Origin header in the request, the Access-Control-Allow-Origin
            header should be echoed back.
        '''
        with self.app.test_client() as c:
            result = c.get('/test_set')

            allowed = result.headers.get('Access-Control-Allow-Headers')
            self.assertTrue(allowed =='Foo, Bar' or allowed =='Bar, Foo') # Order is not garaunteed




if __name__ == "__main__":
     unittest.main()
