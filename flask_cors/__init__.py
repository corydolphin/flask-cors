# -*- coding: utf-8 -*-
"""
    flask_cors
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
import re
import logging
import collections
from datetime import timedelta
from functools import update_wrapper
from six import string_types
from flask import make_response, request, current_app
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from ._version import __version__


# Compatibility with old Pythons!
if not hasattr(logging, 'NullHandler'):
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
    logging.NullHandler = NullHandler

# Response Headers
ACL_ORIGIN = 'Access-Control-Allow-Origin'
ACL_METHODS = 'Access-Control-Allow-Methods'
ACL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACL_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACL_MAX_AGE = 'Access-Control-Max-Age'

# Request Header
ACL_REQUEST_METHOD = 'Access-Control-Request-Method'
ACL_REQUEST_HEADERS = 'Access-Control-Request-Headers'

ALL_METHODS = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']
CONFIG_OPTIONS = ['CORS_ORIGINS', 'CORS_METHODS', 'CORS_ALLOW_HEADERS',
                  'CORS_EXPOSE_HEADERS', 'CORS_SUPPORTS_CREDENTIALS',
                  'CORS_MAX_AGE', 'CORS_SEND_WILDCARD',
                  'CORS_AUTOMATIC_OPTIONS', 'CORS_VARY_HEADER',
                  'CORS_RESOURCES', 'CORS_INTERCEPT_EXCEPTIONS']

# headers was renamed to CORS_ALLOW_HEADERS in v1.11.2
# included for backwards compatibility
CONFIG_OPTIONS.append('CORS_HEADERS')

# Attribute added to request object by decorator to indicate that CORS
# was evaluated, in case the decorator and extension are both applied to a view.
FLASK_CORS_EVALUATED = '_FLASK_CORS_EVALUATED'

# Strange, but this gets the type of a compiled regex, which is otherwise not
# exposed in a public API.
RegexObject = type(re.compile(''))
_defaults_dict = dict(origins='*',
                      methods=ALL_METHODS,
                      allow_headers='*',
                      automatic_options=True,
                      send_wildcard=False,
                      vary_header=True,
                      supports_credentials=False)


def cross_origin(*args, **kwargs):
    '''
    This function is the decorator which is used to wrap a Flask route with.
    In the simplest case, simply use the default parameters to allow all
    origins in what is the most permissive configuration. If this method
    modifies state or performs authentication which may be brute-forced, you
    should add some degree of protection, such as Cross Site Forgery
    Request protection.


    :param origins: The origin, or list of origins to allow requests from.
        The origin(s) may be regular expressions, case-sensitive strings,
        or else an asterisk

        Default : '*'
    :type origins: list, string or regex

    :param methods: The method or list of methods which the allowed origins
        are allowed to access for non-simple requests.

        Default : [GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE]
    :type methods: list or string

    :param expose_headers: The header or list which are safe to expose to the
        API of a CORS API specification.

        Default : None
    :type expose_headers: list or string

    :param allow_headers: The header or list of header field names which can be
        used when this resource is accessed by allowed origins. The header(s)
        may be regular expressions, case-sensitive strings, or else an asterisk.

        Default : '*', allow all headers
    :type allow_headers: list, string or regex

    :param supports_credentials: Allows users to make authenticated requests.
        If true, injects the `Access-Control-Allow-Credentials` header in
        responses. This allows cookies to be submitted across domains.

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

        Default : False
    :type send_wildcard: bool

    :param vary_header: If True, the header Vary: Origin will be returned
        as per the W3 implementation guidelines.

        Setting this header when the `Access-Control-Allow-Origin` is
        dynamically generated (e.g. when there is more than one allowed
        origin, and an Origin than '*' is returned) informs CDNs and other
        caches that the CORS headers are dynamic, and cannot be cached.

        If False, the Vary header will never be injected or altered.

        Default : True
    :type vary_header: bool

    :param automatic_options: Only applies to the `cross_origin` decorator.
        If True, Flask-CORS will override Flask's default OPTIONS handling to
        return CORS headers for OPTIONS requests.

        Default : True
    :type automatic_options: bool


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

            getLogger().debug("Using computed options %s", options)

            if options.get('automatic_options') and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))

            _set_cors_headers(resp, options)
            setattr(resp, FLASK_CORS_EVALUATED, True)
            return resp

        # If True, intercept OPTIONS requests by modifying the view function,
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
    '''
        Initializes Cross Origin Resource sharing for the application. The
        arguments are identical to :py:func:`cross_origin`, with the
        addition of a `resources` parameter. The resources parameter
        defines a series of regular expressions for resource paths to match
        and optionally, the associated options
        to be applied to the particular resource. These options are
        identical to the arguments to :py:func:`cross_origin`.

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

        Default :'*'

        :type resources: dict, iterable or string

    '''

    def __init__(self, app=None, **kwargs):
        self._options = kwargs
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        options = {}
        options.update(_defaults_dict)
        options.update(_get_app_kwarg_dict(app))
        options.update(self._options)
        options.update(kwargs)

        _intercept_exceptions = options.get('intercept_exceptions', True)
        resources = _parse_resources(options.get('resources', [r'/*']))
        resources_human = dict(
            map(
                lambda r: (_get_regexp_pattern(r[0]), r[1]),
                resources
            )
        )

        getLogger(app).info("Configuring CORS with resources and options%s", resources_human)


        def cors_after_request(resp):
            '''
                The actual after-request handler, retains references to the
                the options, and definitions of resources through a closure.
            '''
            # If CORS headers are set in a view decorator, pass
            if resp.headers.get(ACL_ORIGIN):
                getLogger().debug('CORS have been already evaluated, skipping')
                return resp

            for res_regex, res_options in resources:
                if _try_match(request.path, res_regex):
                    _options = options.copy()
                    _options.update(res_options)
                    _serialize_options(_options)
                    getLogger().debug("Request to '%s' matches CORS resource '%s'. Using options: %s",
                        request.path, _get_regexp_pattern(res_regex), _options)
                    _set_cors_headers(resp, _options)
                    break
            else:
                getLogger().debug('No CORS rule matches')
            return resp

        app.after_request(cors_after_request)

        # Wrap exception handlers with cross_origin
        # These error handlers will still respect the behavior of the route
        if _intercept_exceptions:
            def _after_request_decorator(f):
                def wrapped_function(*args, **kwargs):
                    return cors_after_request(app.make_response(f(*args, **kwargs)))
                return wrapped_function

            app.handle_exception = _after_request_decorator(
                app.handle_exception)
            app.handle_user_exception = _after_request_decorator(
                app.handle_user_exception)


def _parse_resources(resources):
    if isinstance(resources, dict):
        # To make the API more consistent with the decorator, allow a
        # resource of '*', which is not actually a valid regexp.
        resources = [(_re_fix(k), v) for k, v in resources.items()]

        # Sort by regex length to provide consistency of matching and
        # to provide a proxy for specificity of match. E.G. longer
        # regular expressions are tried first.
        def pattern_length(pair):
            maybe_regex, _ = pair
            return len(_get_regexp_pattern(maybe_regex))

        return sorted(resources,
                      key=pattern_length,
                      reverse=True)

    elif isinstance(resources, string_types):
        return [(_re_fix(resources), {})]

    elif isinstance(resources, collections.Iterable):
        return [(_re_fix(r), {}) for r in resources]

    # Type of compiled regex is not part of the public API. Test for this
    # at runtime.
    elif isinstance(resources,  RegexObject):
        return [(_re_fix(resources), {})]

    else:
        raise ValueError("Unexpected value for resources argument.")

def _get_regexp_pattern(regexp):
    '''
        Helper that returns regexp pattern from given value.

        :param regexp: regular expression to stringify
        :type regexp: _sre.SRE_Pattern or str
        :returns: string representation of given regexp pattern
        :rtype: str
    '''
    try:
        return regexp.pattern
    except AttributeError:
        return str(regexp)

def _get_cors_origin(options, request_origin):
    origins = options.get('origins')
    wildcard = r'.*' in origins

    # If the Origin header is not present terminate this set of steps.
    # The request is outside the scope of this specification.-- W3Spec
    if request_origin:
        getLogger().debug("CORS request received with 'Origin' %s", request_origin)

        # If the allowed origins is an asterisk or 'wildcard', always match
        if wildcard and options.get('send_wildcard'):
            getLogger().debug("Allowed origins are set to '*', assuming valid request")
            return '*'
        # If the value of the Origin header is a case-sensitive match
        # for any of the values in list of origins
        elif _try_match_any(request_origin, origins):
            getLogger().debug("Given origin matches set of allowed origins")
            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            # -- W3Spec
            return request_origin
        else:
            getLogger().debug("Given origin does not match any of allowed origins: %s",
                         map(_get_regexp_pattern, origins))
            return None
    # Terminate these steps, return the original request untouched.
    else:
        getLogger().debug("'Origin' header was not set, which means CORS was not requested, skipping")
        return None

def _get_allow_headers(options, acl_request_headers):
    if acl_request_headers:
        acl_request_headers = [h.strip() for h in acl_request_headers.split(',')] # remove falsey values
        matching_headers = filter(
            lambda h: _try_match_any(h, options.get('allow_headers')), # any header that matches in the allow_headers
            acl_request_headers
        )
        return ', '.join(sorted(matching_headers))

    return None


def _get_cors_headers(options, request_headers, request_method, response_headers):
    origin_to_set = _get_cors_origin(options, request_headers.get('Origin'))
    headers = {}

    if origin_to_set is None:  # CORS is not enabled for this route
        return headers
    getLogger().info("Request from Origin:%s, setting %s:%s",
                     request_headers.get('Origin'), ACL_ORIGIN, origin_to_set)

    headers[ACL_ORIGIN] = origin_to_set
    headers[ACL_EXPOSE_HEADERS] = options.get('expose_headers')

    if options.get('supports_credentials'):
        headers[ACL_CREDENTIALS] = 'true'  # case sensative

    # This is a preflight request
    # http://www.w3.org/TR/cors/#resource-preflight-requests
    if request_method == 'OPTIONS':
        acl_request_method = request_headers.get(ACL_REQUEST_METHOD, '').upper()

        # If there is no Access-Control-Request-Method header or if parsing
        # failed, do not set any additional headers
        if acl_request_method and acl_request_method in options.get('methods'):

            # If method is not a case-sensitive match for any of the values in
            # list of methods do not set any additional headers and terminate this set of steps.
            headers[ACL_ALLOW_HEADERS] = _get_allow_headers(options, request_headers.get(ACL_REQUEST_HEADERS))
            headers[ACL_MAX_AGE] = options.get('max_age')
            headers[ACL_METHODS] = options.get('methods')
        else:
            getLogger().info("Access-Control-Request-Method:%s does not match allowed methods %s",
                             acl_request_method, options.get('methods'))

    # http://www.w3.org/TR/cors/#resource-implementation
    if options.get('vary_header'):
        # Only set header if the origin returned will vary dynamically,
        # i.e. if we are not returning an asterisk, and there are multiple
        # origins that can be matched.
        if headers[ACL_ORIGIN] != '*' and len(options.get('origins')) > 1:
            vary = ['Origin', response_headers.get('Vary')]
            headers['Vary'] = ', '. join(v for v in vary if v is not None)

    return dict((k, v) for k, v in headers.items() if v)


def _set_cors_headers(resp, options):
    '''
        Performs the actual evaluation of Flas-CORS options and actually
        modifies the response object.

        This function is used both in the decorator and the after_request
        callback
    '''

    # If CORS has already been evaluated via the decorator, skip
    if hasattr(resp, FLASK_CORS_EVALUATED):
        getLogger().debug('CORS have been already evaluated, skipping')
        return resp

    headers_to_set = _get_cors_headers(options,
                                       request.headers,
                                       request.method,
                                       resp.headers)
    getLogger().debug('Settings CORS headers: %s', str(headers_to_set))

    for k, v in headers_to_set.items():
        resp.headers[k] = v

    return resp


def _get_app_kwarg_dict(appInstance=None):
    '''
        Returns the dictionary of CORS specific app configurations.
    '''
    app = (appInstance or current_app)
    return dict(
        (k.lower().replace('cors_', ''), app.config.get(k))
        for k in CONFIG_OPTIONS
        if app.config.get(k) is not None
    )


def _re_fix(reg):
    '''
        Replace the invalid regex r'*' with the valid, wildcard regex r'/.*' to
        enable the CORS app extension to have a more user friendly api.
    '''
    return r'.*' if reg == r'*' else reg

def _try_match_any(inst, patterns):
    return any(_try_match(inst, pattern) for pattern in patterns)


def _try_match(request_origin, pattern):
    '''
        Safely attempts to match a pattern or string to a request origin.
    '''
    try:
        return re.match(pattern, request_origin)
    except:
        return request_origin == pattern


def _flexible_str(obj):
    '''
        A more flexible str function which intelligently handles
        stringifying iterables. The results are lexographically
        sorted to ensure generated responses are consistent when
        iterables such as Set are used (whose order is usually platform
        dependent)
    '''
    if(not isinstance(obj, string_types)
            and isinstance(obj, collections.Iterable)):
        return ', '.join(str(item) for item in sorted(obj))
    else:
        return str(obj)


def _serialize_option(options_dict, key, upper=False):
    if key in options_dict:
        value = _flexible_str(options_dict[key])
        options_dict[key] = value.upper() if upper else value

def _ensure_iterable(inst):
    '''
        Wraps scalars or string types as a list, or returns the iterable instance.

    '''
    if isinstance(inst, string_types):
        return [inst]
    elif not isinstance(inst, collections.Iterable):
        return [inst]
    else:
        return inst


def _sanitize_regex_param(param):
    return [_re_fix(x) for x in _ensure_iterable(param)]


def _serialize_options(options):
    '''
        A helper method to serialize and processes the options dictionary
        where applicable.
    '''

    # Ensure origins is a list of allowed origins with at least one entry.
    options['origins'] = _sanitize_regex_param(options.get('origins'))
    options['allow_headers'] = _sanitize_regex_param(options.get('allow_headers'))

    # This is expressly forbidden by the spec. Raise a value error so people don't
    # get burned in production.
    if r'.*' in options['origins'] and options['supports_credentials'] and options['send_wildcard']:
        raise ValueError("Cannot use supports_credentials in conjunction with"
            "an origin string of '*'. See: http://www.w3.org/TR/cors/#resource-requests")

    _serialize_option(options, 'expose_headers')
    _serialize_option(options, 'methods', upper=True)

    if isinstance(options.get('max_age'), timedelta):
        options['max_age'] = str(int(options['max_age'].total_seconds()))


def getLogger(app=None):
    if stack.top is not None: # we are in the context of a request
        return logging.getLogger("%s.cors" % current_app.logger_name)
    elif app is not None: # For use init method, when an app is known, but there is no context
        return logging.getLogger("%s.cors" % app.logger_name)
    else:
        return logging.getLogger("flask.ext.cors")
