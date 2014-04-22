# -*- coding: utf-8 -*-
"""
    flask_cors
    ~~~~~~~~~~

    Flask-CORS extension module
"""
from _version import __version__
import collections

from datetime import timedelta
from functools import update_wrapper

from flask import make_response, request, current_app
from six import string_types

AccessControlAllowOrigin = 'Access-Control-Allow-Origin'


def cross_origin(origins=None, methods=None, headers=None,
                 supports_credentials=False, max_age=None, send_wildcard=True,
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
    methods = methods or ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT']
    methods = ', '.join(sorted(x for x in methods)).upper()

    if (not isinstance(headers, string_types)
            and isinstance(headers, collections.Iterable)):
        headers = ', '.join(x for x in headers)

    wildcard = origins == '*'

    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            # Determine origins when in the context of a request
            origins = _origins or current_app.config.get('CORS_ORIGINS', '*')
            origins_str = str(origins)

            if(not isinstance(origins, string_types)
                    and isinstance(origins, collections.Iterable)):
                origins_str = ', '.join(origins)

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
            else:
                resp = make_response(f(*args, **kwargs))

            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            if wildcard:
                # If the `origins` param is '*', either send the request's
                # origin, or `*`
                if send_wildcard:
                    resp.headers[AccessControlAllowOrigin] = origins
                else:
                    req_origin = request.headers.get('Origin', '*')
                    resp.headers[AccessControlAllowOrigin] = req_origin

            # If not 'wildcard', send the string-joined-form of the
            # origins header
            else:
                resp.headers[AccessControlAllowOrigin] = origins_str

            resp.headers['Access-Control-Allow-Methods'] = methods
            if max_age:
                resp.headers['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                resp.headers['Access-Control-Allow-Headers'] = headers
            if supports_credentials:
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
            return resp

        # If True, intercept OPTIONS requests by modifying the view function
        # mirroring Flask's default behavior, and wrapping the response with
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
