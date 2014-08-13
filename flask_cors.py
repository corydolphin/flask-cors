# -*- coding: utf-8 -*-
"""
    flask_cors
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
import collections
from datetime import timedelta
import re
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

CONFIG_OPTIONS = ['CORS_ORIGINS', 'CORS_METHODS', 'CORS_HEADERS',
                  'CORS_EXPOSE_HEADERS', 'CORS_SUPPORTS_CREDENTIALS',
                  'CORS_MAX_AGE', 'CORS_SEND_WILDCARD', 'CORS_ALWAYS_SEND',
                  'CORS_AUTOMATIC_OPTIONS', 'CORS_VARY_HEADER']

_defaults_dict = dict(origins='*',
                      always_send=True,
                      automatic_options=True,
                      send_wildcard=True,
                      vary_header=True)


def cross_origin(*args, **kwargs):
    '''
    This function is the decorator which is used to wrap a Flask route with.
    In the simplest case, simply use the default parameters to allow all
    origins in what is the most permissive configuration. If this method
    modifies state or performs authentication which may be brute-forced, you
    should add some degree of protection, such as Cross Site Forgery
    Request protection.


    :param origins: The origin, or list of origins to allow requests from.
    :type origins: list or string

    :param methods: The method or list of methods which the allowed origins
        are allowed to access.
    :type methods: list

    :param headers: The header or list of header field names which can be used
        when this resource is accessed by allowed origins.
    :type headers: list or string

    :param expose_headers: The header or list of headers which are are safe to
        expose to browsers.
    :type headers: list or string

    :param supports_credentials: Allows users to make authenticated requests.
        If true, injects the `Access-Control-Allow-Credentials` header in
        responses.
        Note: According to the W3 spec, this option cannot be used in
        conjuction with a '*' origin

    :type supports_credentials: bool

    :param max_age: The maximum time for which this CORS request maybe cached.
        This value is set as the `Access-Control-Max-Age` header.
    :type max_age: timedelta, integer, string or None

    :param send_wildcard: If True, and the origins parameter is `*`, a
        wildcard `Access-Control-Allow-Origin` header is sent, rather than
        the request's `Origin` header.
    :type send_wildcard: bool

    :param always_send: If True, CORS headers are sent even if there is no
                        `Origin` in the request's headers.
    :type always_send: bool

    :param automatic_options: If True, CORS headers will be returned for
        OPTIONS requests. For use with cross domain POST requests which
        preflight OPTIONS requests, you will need to specifically allow
        the Content-Type header.
    :type automatic_options: bool

    :param vary_header: If True, the header Vary: Origin will be returned
        as per suggestion by the W3 implementation guidelines. Setting this
        header when the `Access-Control-Allow-Origin` is dynamically generated
        e.g. when there is more than one allowed origin, and any Origin other
        than '*' is returned, informing CDNs and other caches that the CORS
        headers are dynamic, and cannot be re-used.
        If False, the Vary header will never be injected or altered.
    :type vary_header: bool

    '''

    _options = kwargs

    def decorator(f):
        def wrapped_function(*args, **kwargs):

            # Handle setting of Flask-Cors parameters
            options = {}
            options.update(_defaults_dict)
            options.update(_get_app_kwarg_dict())
            options.update(_options)
            _serialize_options(options)

            if options.get('automatic_options') and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))

            _set_cors_headers(resp, options)

            return resp

        # If True, intercept OPTIONS requests by modifying the view function
        # replicating Flask's default behavior, and wrapping the response with
        # CORS headers.
        #
        # If f.provide_automatic_options is unset or True, Flask's route
        # decorator (which is actually wraps the function object we return)
        # intercepts OPTIONS handling, and requests will not have CORS headers
        if _options.get('automatic_options', True):
            f.required_methods = getattr(f, 'required_methods', set())
            f.required_methods.add('OPTIONS')
            f.provide_automatic_options = False

        return update_wrapper(wrapped_function, f)
    return decorator


class CORS(object):
    def __init__(self, app=None, **kwargs):
        '''
            Initializes Cross Origin Resource sharing for the application. The
            arguments are identical to :py:func:`cross_origin`, with the
            addition of a `resources` parameter. The resources parameter
            defines a series of regular expressions for resource paths to match
            and optionally, the associated :py:func:`cross_origin` options
            to be applied to the particular resource.

            The settings for CORS are determined in the following order:
                Resource level settings (e.g when passed as a dictionary)
                Keyword argument settings
                App level configuration settings (e.g. CORS_*)
                Default settings

            Note: as it is possible for multiple regular expressions to match a
            resource path, the regular expressions are first sorted by length,
            from longest to shortest, in order to attempt to match the most
            specific regular expression. This allows the definition of a
            number of specific resource options, with a wildcard fallback
            for all other resources.

            :param resources: the series of regular expression and (optionally)
            associated CORS options to be applied to the given resource path.

            If the argument is a dictionary, it is expected to be of the form:
            regexp : dict_of_options

            If the argument is a list, it is expected to be a list of regular
            expressions, for which the app-wide configured options are applied.

            If the argument is a string, it is expected to be a regular
            expression for which the app-wide configured options are applied.
            :type resources: dict, iterable or string

        '''

        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        options = {}
        options.update(_defaults_dict)
        options.update(_get_app_kwarg_dict(app))
        options.update(kwargs)

        _kwarg_resources = kwargs.get('resources')
        _app_resources = app.config.get('CORS_RESOURCES')
        _resources = _kwarg_resources or _app_resources or [r'/*']

        if isinstance(_resources, dict):  # sort the regexps by length
            resources = sorted(_resources.items(),
                               key=lambda r: len(r[0]),
                               reverse=True
                               )
        elif isinstance(_resources, string_types):
            resources = [(_resources, {})]
        elif isinstance(_resources, collections.Iterable):
            resources = [(r, {}) for r in _resources]
        else:
            raise ValueError("Unexpected value for resources argument.")

        def cors_after_request(resp):
            '''
                The actual after-request handler, retains references to the
                the options, and definitions of resources through a closure.
            '''
            # If CORS headers are set in a view decorator, pass
            if resp.headers.get(ACL_ORIGIN):
                return resp

            for res_regex, res_options in resources:
                if re.match(res_regex, request.path):
                    _options = options.copy()
                    _options.update(res_options)
                    _serialize_options(_options)
                    _set_cors_headers(resp, _options)
                    break
            return resp

        app.after_request(cors_after_request)


def _set_cors_headers(resp, options):
    request_origin = request.headers.get('Origin', None)
    wildcard = options.get('origins') == '*'

    # If the Origin header is not present terminate this set of steps.
    # The request is outside the scope of this specification.-- W3Spec
    #
    # Unless always_send is set, then ignore W3 spec
    if request_origin or options.get('always_send'):
         # If the value of the Origin header is a case-sensitive match
         # for any of the values in list of origins
        if request_origin and request_origin in options.get('origins'):
            resp.headers[ACL_ORIGIN] = request_origin
            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            # -- W3Spec

        # If the allowed origins is an asterisk or 'wildcard', always match
        elif wildcard:
            if options.get('send_wildcard'):
                resp.headers[ACL_ORIGIN] = '*'
            else:
                resp.headers[ACL_ORIGIN] = request_origin
        else:
            resp.headers[ACL_ORIGIN] = options.get('origins')

        if options.get('methods'):
            resp.headers[ACL_METHODS] = options.get('methods')

        if options.get('headers'):
            resp.headers[ACL_HEADERS] = options.get('headers')

        if options.get('expose_headers'):
            resp.headers[ACL_EXPOSE_HEADERS] = options.get(
                'expose_headers')

        if options.get('max_age'):
            resp.headers[ACL_MAX_AGE] = options.get('max_age')

        if options.get('supports_credentials'):
            resp.headers[ACL_CREDENTIALS] = 'true'

        if request.method == 'OPTIONS':
            resp.headers[ACL_METHODS] = options.get('methods', _flexible_str(
                ALL_METHODS))

        # http://www.w3.org/TR/cors/#resource-implementation
        if resp.headers[ACL_ORIGIN] != '*' and options.get('vary_header'):
            vary = ['Origin', resp.headers.get('Vary', None)]
            resp.headers['Vary'] = ', '. join(v for v in vary if v is not None)


def _get_app_kwarg_dict(app=current_app):
    return dict([
                (k.lower().replace('cors_', ''), app.config.get(k))
                for k in CONFIG_OPTIONS
                if app.config.get(k) is not None
                ])


def _flexible_str(obj):
    if(not isinstance(obj, string_types)
            and isinstance(obj, collections.Iterable)):
        return ', '.join(str(item) for item in sorted(obj))
    else:
        return str(obj)


def _serialize_option(d, key, upper=False):
    if key in d:
        d[key] = _flexible_str(d[key])
        if upper:
            if d[key]:
                d[key].upper()


def _serialize_options(options):
    _serialize_option(options, 'methods', upper=True)
    _serialize_option(options, 'origins')
    _serialize_option(options, 'headers')
    _serialize_option(options, 'expose_headers')

    if isinstance(options.get('max_age'), timedelta):
        options['max_age'] = str(int(options['max_age'].total_seconds()))
