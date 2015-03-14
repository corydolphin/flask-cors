# -*- coding: utf-8 -*-
"""
    flask_cors
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""
from flask import request
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from .core import *


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
        options.update(DEFAULT_OPTIONS)
        options.update(get_app_kwarg_dict(app))
        options.update(self._options)
        options.update(kwargs)

        _intercept_exceptions = options.get('intercept_exceptions', True)
        resources = parse_resources(options.get('resources', [r'/*']))
        resources_human = dict(
            map(
                lambda r: (get_regexp_pattern(r[0]), r[1]),
                resources
            )
        )

        getLogger(app).info("Configuring CORS with resources and options%s",
                            resources_human)

        def cors_after_request(resp):
            '''
                The actual after-request handler, retains references to the
                the options, and definitions of resources through a closure.
            '''
            # If CORS headers are set in a view decorator, pass
            if resp.headers.get(ACL_ORIGIN):
                debug('CORS have been already evaluated, skipping')
                return resp

            for res_regex, res_options in resources:
                if try_match(request.path, res_regex):
                    resource_options = options.copy()
                    resource_options.update(res_options)
                    resource_options = serialize_options(resource_options)
                    debug("Request to '%s' matches CORS resource '%s'. Using options: %s",
                          request.path, get_regexp_pattern(res_regex), resource_options)
                    set_cors_headers(resp, resource_options)
                    break
            else:
                debug('No CORS rule matches')
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
