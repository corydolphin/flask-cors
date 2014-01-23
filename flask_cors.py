from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from six import string_types
import collections

AccessControlAllowOrigin = 'Access-Control-Allow-Origin'

def cross_origin(origins='*', methods=['GET','HEAD','POST','OPTIONS','PUT'],
           headers=None, supports_credentials=False, max_age=None, 
           send_wildcard=True, always_send=True, automatic_options=False):
    '''
    This function is the decorator which is used to wrap a Flask route with. In
    the simplest case, simply use the default parameters to allow all origins
    in what is the most permissive configuration. If this method modifies state
    or performs authentication which may be brute-forced, you should add some
    degree of perfection, for example Cross Site Forgery Request protection.
     

    :param origins: The origin, or list of origins which are to be allowed,
        and injected into the returned `Access-Control-Allow-Origin` header
    :type origins: list or string

    :param methods: The methods to be allowed and injected `Access-Control-Allow-Methods`.
    :type methods: list

    :param headers: The list of allowed headers to be injected in  `Access-Control-Allow-Headers`.
    :type headers: list or string

    :param supports_credentials: TODO. Currently unusued, May be implemented in the future.
    :type supports_credentials: bool

    :param max_age: The maximum time for which this CORS request may be cached. This value is set as the `Access-Control-Max-Age` header.
    :type max_age: timedelta, integer, string or None

    :param send_wildcard: If True, and the origins parameter is `*`, a wildcard `Access-Control-Allow-Origin` header is sent, rather than echoing the request's `Origin` header.
    :type send_wildcard: bool

    :param always_send: If True, CORS headers are sent even if there is no `Origin` in the request's headers. 
    :type always_send: bool

    :param automatic_options: If True, Flask's automatic_options is enabled, otherwise default Flask-Cors behavior is used.
    :type automatic_options: bool

    '''

    methods = methods or ['GET','HEAD','POST','OPTIONS','PUT']
    methods = ', '.join(sorted(x for x in methods)).upper()


    if not isinstance(headers, string_types) and isinstance(headers, collections.Iterable):
        headers = ', '.join(x for x in headers)

    if not isinstance(headers, string_types) and isinstance(headers, collections.Iterable):
        origins = ', '.join(origins)

    wildcard = origins == '*'

    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            # If the Origin header is not present terminate this set of steps. 
            # The request is outside the scope of this specification.
            if not 'Origin' in request.headers and not always_send:
                return make_response(f(*args, **kwargs))

            # If the value of the Origin header is not a case-sensitive match
            # for any of the values in list of origins, do not set any additional
            # headers and terminate this set of steps.
            elif not wildcard and not always_send and not request.headers.get('Origin', '') in origins:
                return make_response(f(*args, **kwargs))

            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))


            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            if wildcard:
                # If the `origins` param is '*', either send the request's origin, or `*`
                if send_wildcard:
                    resp.headers[AccessControlAllowOrigin] = origins
                else:
                    resp.headers[AccessControlAllowOrigin] = request.headers.get('Origin', '*')
            else:
                resp.headers[AccessControlAllowOrigin] = request.headers.get('Origin')


            resp.headers['Access-Control-Allow-Methods'] = methods
            if max_age:
                resp.headers['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                resp.headers['Access-Control-Allow-Headers'] = headers
            return resp

        f.required_methods = ['OPTIONS']
        f.provide_automatic_options = automatic_options # Override Flask's default OPTIONS handling

        return update_wrapper(wrapped_function, f)
    return decorator