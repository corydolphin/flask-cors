from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

AccessControlAllowOrigin = 'Access-Control-Allow-Origin'

def cross_origin(origins='*', methods=['GET','HEAD','POST','OPTIONS','PUT'],
           headers=None, supports_credentials=True, max_age=None, 
           send_wildcard=True, always_send=True, automatic_options=False):
    '''
    This function is the decorator which is used to wrap a Flask route with.
    :param origins: The origin, or list of origins which are to be allowed,
        and injected into the returned `Access-Control-Allow-Origin` header
    :type origins: :class:`list` or `string`

    :param methods: The methods to be allowed and injected `Access-Control-Allow-Methods`.
    :type add_context_processor: bool
    '''

    methods = methods or ['GET','HEAD','POST','OPTIONS','PUT']
    methods = ', '.join(sorted(x.upper() for x in methods))

    if headers is not None and isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origins, basestring):
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

            h = resp.headers

            # Add a single Access-Control-Allow-Origin header, with either
            # the value of the Origin header or the string "*" as value.
            if wildcard:
                # If the `origins` param is '*', either send the request's origin, or `*`
                if send_wildcard:
                    h[AccessControlAllowOrigin] = origins
                else:
                    h[AccessControlAllowOrigin] = request.headers.get('Origin', '*')
            else:
                h[AccessControlAllowOrigin] = request.headers.get('Origin')


            h['Access-Control-Allow-Methods'] = methods
            if max_age:
                h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.required_methods = ['OPTIONS']
        f.provide_automatic_options = automatic_options # Override Flask's default OPTIONS handling

        return update_wrapper(wrapped_function, f)
    return decorator