# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
import collections
from datetime import timedelta
from functools import update_wrapper

from flask import make_response, request, current_app
from six import string_types

# Common string constants
ACL_ORIGIN = 'Access-Control-Allow-Origin'
ACL_METHODS = 'Access-Control-Allow-Methods'
ACL_HEADERS = 'Access-Control-Allow-Headers'
ACL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACL_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACL_MAX_AGE = 'Access-Control-Max-Age'


ALL_METHODS = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT']
ALL_METHODS_STR = ', '.join(sorted(ALL_METHODS)).upper()


def cross_origin(origins=None, methods=None, headers=None, expose_headers=None,
                 supports_credentials=False,  max_age=None, send_wildcard=True,
                 always_send=True, automatic_options=True):
    '''
    This function is the decorator which is used to wrap a Flask route with.
    In the simplest case, simply use the default parameters to allow all
    origins in what is the most permissive configuration. If this method
    modifies state or performs authentication which may be brute-forced, you
    should add some degree of protection, for example Cross Site Forgery
    Request protection.


    :param origins: The origin, or list of origins which are to be allowed,
        and injected into the returned `Access-Control-Allow-Origin` header
    :type origins: list or string

    :param methods: The methods to be allowed and injected as the
        `Access-Control-Allow-Methods` header returned.
    :type methods: list

    :param headers: The list of allowed headers to be injected as the
        `Access-Control-Allow-Headers` header returned.
    :type headers: list or string

    :param expose_headers: The list of headers to be exposed to browsers
        through the  `Access-Control-Expose-Headers` header returned.
    :type headers: list or string

    :param supports_credentials: Allows users to make authenticated requests.
        If true, injects the `Access-Control-Allow-Credentials` header in
        responses.
         Note: this option cannot be used in conjuction with a '*' origin
    :type supports_credentials: bool

    :param max_age: The maximum time for which this CORS request maybe cached.
                    This value is set as the `Access-Control-Max-Age` header.
    :type max_age: timedelta, integer, string or None

    :param send_wildcard: If True, and the origins parameter is `*`, a
                          wildcard `Access-Control-Allow-Origin` header is
                          sent, rather than echoing the request's `Origin`
                          header.
    :type send_wildcard: bool

    :param always_send: If True, CORS headers are sent even if there is no
                        `Origin` in the request's headers.
    :type always_send: bool

    :param automatic_options: If True, CORS headers will be returned for
        OPTIONS requests. For use with cross domain POST requests which
        preflight OPTIONS requests, you will need to specifically allow
        the Content-Type header.
    :type automatic_options: bool

    '''
    _origins = origins
    _methods = methods
    _headers = headers
    _expose_headers = expose_headers
    _credentials = supports_credentials
    _max_age = max_age
    _send_wildcard = send_wildcard
    _always_send = always_send
    _automatic_options = automatic_options

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            # Handle setting of Flask-Cors parameters
            _app_origins = current_app.config.get('CORS_ORIGINS')
            _app_methods = current_app.config.get('CORS_METHODS')
            _app_headers = current_app.config.get('CORS_HEADERS')
            _app_expose_headers = current_app.config.get('CORS_EXPOSE_HEADERS')
            _app_credentials = current_app.config.get(
                'CORS_SUPPORTS_CREDENTIALS')
            _app_max_age = current_app.config.get('CORS_MAX_AGE')
            _app_send_wildcard = current_app.config.get(
                'CORS_SEND_WILDCARD')
            _app_always_send = current_app.config.get('CORS_ALWAYS_SEND')
            _app_automatic_options = current_app.config.get(
                'CORS_AUTOMATIC_OPTIONS'
            )

            # Default origins is wildcard
            origins = _origins or _app_origins or '*'
            origins_str = _flexible_str(origins, sort=True)
            wildcard = origins_str == '*'

            methods = _methods or _app_methods
            if methods is not None:
                methods = _flexible_str(methods, sort=True).upper()

            headers = _headers or _app_headers
            if headers is not None:
                headers = _flexible_str(headers, sort=True)

            expose_headers = _expose_headers or _app_expose_headers
            if expose_headers is not None:
                expose_headers = _flexible_str(expose_headers, sort=True)

            supports_credentials = _credentials or _app_credentials

            max_age = _max_age or _app_max_age
            if isinstance(max_age, timedelta):
                max_age = int(max_age.total_seconds())

            send_wildcard = _send_wildcard or _app_send_wildcard

            always_send = _always_send or _app_always_send

            automatic_options = _automatic_options or _app_automatic_options

            # Begin actual CORS handling
            # If the Origin header is not present terminate this set of steps.
            # The request is outside the scope of this specification.
            request_origin = request.headers.get('Origin', '')

            if 'Origin' not in request.headers and not always_send:
                return make_response(f(*args, **kwargs))

            # If the value of the Origin header is not a case-sensitive match
            # for any of the values in list of origins, do not set any
            # additional headers and terminate this set of steps.
            elif(not wildcard and not always_send and
                    request_origin not in origins):
                return make_response(f(*args, **kwargs))

            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
                resp.headers[ACL_METHODS] = methods or ALL_METHODS_STR
            else:
                resp = make_response(f(*args, **kwargs))

            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            if wildcard:
                if send_wildcard:
                    resp.headers[ACL_ORIGIN] = origins
                else:
                    resp.headers[ACL_ORIGIN] = request_origin

            # If not 'wildcard', send the string-joined-form of the
            # origins header
            else:
                resp.headers[ACL_ORIGIN] = origins_str

            if methods is not None:
                resp.headers[ACL_METHODS] = methods

            if headers is not None:
                resp.headers[ACL_HEADERS] = headers

            if expose_headers is not None:
                resp.headers[ACL_EXPOSE_HEADERS] = expose_headers

            if max_age is not None:
                resp.headers[ACL_MAX_AGE] = max_age

            if supports_credentials:
                resp.headers[ACL_CREDENTIALS] = 'true'

            return resp

        # If True, intercept OPTIONS requests by modifying the view function
        # replicating Flask's default behavior, and wrapping the response with
        # CORS headers.
        #
        # If f.provide_automatic_options is unset or True, Flask's route
        # decorator (which is actually wraps the function object we return)
        # intercepts OPTIONS handling, and requests will not have CORS headers
        if automatic_options:
            f.required_methods = getattr(f, 'required_methods', set())
            f.required_methods.add('OPTIONS')
            f.provide_automatic_options = False

        return update_wrapper(wrapped_function, f)
    return decorator


def _flexible_str(obj, sort=False):
    if(not isinstance(obj, string_types)
            and isinstance(obj, collections.Iterable)):
        if sort:
            return ', '.join(str(item) for item in sorted(obj))
        else:
            return ', '.join(str(item) for item in obj)
    else:
        return str(obj)
