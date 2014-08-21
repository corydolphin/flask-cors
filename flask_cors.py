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


ALL_METHODS = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']

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
        The origin(s) may be regular expressions, exact origins, or else an
        asterisk.

        Default : '*'
    :type origins: list or string

    :param methods: The method or list of methods which the allowed origins
        are allowed to access.

        Default : [GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE]
    :type methods: list or string

    :param headers: The header or list of header field names which can be used
        when this resource is accessed by allowed origins.

        Default : None
    :type headers: list or string

    :param expose_headers: The header or list of headers which are are safe to
        expose to browsers.

        Default : None
    :type expose_headers: list or string

    :param supports_credentials: Allows users to make authenticated requests.
        If true, injects the `Access-Control-Allow-Credentials` header in
        responses.

        :note: This option cannot be used in conjuction with a '*' origin

        Default : False
    :type supports_credentials: bool

    :param max_age: The maximum time for which this CORS request maybe cached.
        This value is set as the `Access-Control-Max-Age` header.

        Default : None
    :type max_age: timedelta, integer, string or None

    :param send_wildcard: If True, and the origins parameter is `*`, a
        wildcard `Access-Control-Allow-Origin` header is sent, rather than
        the request's `Origin` header.

        Default : True
    :type send_wildcard: bool

    :param always_send: If True, CORS headers are sent even if there is no
        `Origin` in the request's headers.

        Default : True
    :type always_send: bool

    :param automatic_options: If True, CORS headers will be returned for
        OPTIONS requests. For use with cross domain POST requests which
        preflight OPTIONS requests, you will need to specifically allow
        the Content-Type header.

        Default : True
    :type automatic_options: bool

    :param vary_header: If True, the header Vary: Origin will be returned
        as per suggestion by the W3 implementation guidelines.

        Setting this header when the `Access-Control-Allow-Origin` is
        dynamically generated (e.g. when there is more than one allowed
        origin, and an Origin than '*' is returned) informs CDNs and other
        caches that the CORS headers are dynamic, and cannot be re-used.

        If False, the Vary header will never be injected or altered.

        Default : True
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
            resp._FLASK_CORS_EVALUATED = True  # Mark response as evaluated

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
    '''
        Performs the actual evaluation of Flas-CORS options and actually
        modifies the response object.

        This function is used both in the decorator and the after_request
        callback
    '''

    # If CORS has already been evaluated via the decorator, skip
    if hasattr(resp, '_FLASK_CORS_EVALUATED'):
        return resp

    request_origin = request.headers.get('Origin', None)
    origins = options.get('origins')
    wildcard = '*' in origins
    # If the Origin header is not present terminate this set of steps.
    # The request is outside the scope of this specification.-- W3Spec
    if request_origin:

        # If the allowed origins is an asterisk or 'wildcard', always match
        if wildcard:
            if options.get('send_wildcard'):
                resp.headers[ACL_ORIGIN] = '*'
            else:
                resp.headers[ACL_ORIGIN] = request_origin

        # If the value of the Origin header is a case-sensitive match
        # for any of the values in list of origins
        elif any(_try_match(pattern, request_origin) for pattern in origins):
            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            # -- W3Spec
            resp.headers[ACL_ORIGIN] = request_origin
        else:
            return resp

    # Unless always_send is set, then ignore W3 spec as long as there is a
    # valid list of origins, e.g. one that is not merely comrpised of regular
    # expressions.
    elif options.get('always_send') and options.get('origins_str'):
        resp.headers[ACL_ORIGIN] = options.get('origins_str')
    # Terminate these steps, return the original request untouched.
    else:
        return resp

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
        resp.headers[ACL_METHODS] = options.get('methods',
                                                _flexible_str(ALL_METHODS))

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


def _try_match(pattern, request_origin):
    '''
        Safely attempts to match a pattern or string to a request origin.

        If a pattern is an illegal regular expression
    '''
    try:
        return re.match(pattern, request_origin)
    except:
        return request_origin == pattern


def _flexible_str(obj):
    if(not isinstance(obj, string_types)
            and isinstance(obj, collections.Iterable)):
        return ', '.join(str(item) for item in sorted(obj))
    else:
        return str(obj)


def _serialize_option(d, key, target_key=None, upper=False):
    if key in d:
        v = _flexible_str(d[key])
        if upper and v:
            v.upper()
        d[target_key or key] = v


def _is_regexp(pattern):
    '''
        Returns True if the `pattern` is likely to be a regexp,
    '''
    if pattern != '*' and any(c in pattern for c in '?*'):
        return True
    return False


def _filter_false(predicate, iterable):
    '''
        Returns all objects in iterable for which predicate is false.
        Equivalent to the Python 3 version of itertools.filterfalse
    '''
    return filter(lambda x: not predicate(x), iterable)


def _serialize_options(options):
    '''
        A helper method to serialize and processes the options dictionary
        where applicable.
    '''
    # ensure origins is a list of allowed origins with at least one entry.
    if isinstance(options.get('origins'), string_types):
        options['origins'] = [options.get('origins')]

    # remove regular expressions from the list of serialized origins to be
    # returned in the case of a request with no Origin header, while
    # always_send is set to True
    options['origins_str'] = _filter_false(_is_regexp, options.get('origins'))

    _serialize_option(options, 'origins_str')
    _serialize_option(options, 'methods', upper=True)
    _serialize_option(options, 'headers')
    _serialize_option(options, 'expose_headers')

    if isinstance(options.get('max_age'), timedelta):
        options['max_age'] = str(int(options['max_age'].total_seconds()))
