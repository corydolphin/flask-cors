# Flask-CORS

[![Build Status](https://api.travis-ci.org/CoryDolphin/flask-cors.svg?branch=master)](https://travis-ci.org/CoryDolphin/flask-cors) [![Latest Version](https://pypip.in/version/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/) [![Downloads](https://pypip.in/download/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/) [![Supported Python versions](https://pypip.in/py_versions/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/) [![License](https://pypip.in/license/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/)

A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.

## Installation

Install the extension with using pip, or easy_install.

```bash
$ pip install -U flask-cors
```

## Usage

This extension enables CORS support either via a decorator, or a Flask extension. There are three examples shown in the [examples](https://github.com/wcdolphin/flask-cors/tree/master/examples) directory, showing the major use cases. The suggested configuration is the [simple_example.py](https://github.com/wcdolphin/flask-cors/tree/master/examples/simple_example.py), or the [app_example.py](https://github.com/wcdolphin/flask-cors/tree/master/examples/app_based_example.py).


### Simple Usage

In the simplest case, initialize the Flask-Cors extension with default arguments in order to allow CORS on all routes.

```python

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"
```

#### Resource specific CORS

Alternatively, a list of resources and associated settings for CORS can be supplied, selectively enables CORS support on a set of paths on your app.

Note: this resources parameter can also be set in your application's config.

```python
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/v1/users")
def list_users():
  return "user example"
```

#### Route specific CORS via decorator

This extension also exposes a simple decorator to decorate flask routes with. Simply add `@cross_origin()` below a call to Flask's `@app.route(..)` incanation to accept the default options and allow CORS on a given route.

```python
@app.route("/")
@cross_origin() # allow all origins all methods.
def helloWorld():
  return "Hello, cross-origin-world!"
```

#### Logging

Flask-Cors uses standard Python logging, using the module name 'Flask-Cors'. You can read more about logging from [Flask's documentation](http://flask.pocoo.org/docs/0.10/errorhandling/). To add logging for flask_cors to the standard StreamHandler:

```python
for logger in (app.logger, logging.getLogger('Flask-Cors')):
    sh = logging.StreamHandler()
    sh.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)
```

### Options

#### origins
> Default : '*'

The origin, or list of origins to allow requests from. The origin(s) may be regular expressions, exact origins, or else an asterisk.

#### methods
> Default : [GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE]

The method or list of methods which the allowed origins are allowed to access for non-simple requests.

#### expose_headers
> Default : None

The header or list of headers which are safe to expose to the API of a CORS API specification

#### allow_headers
> Default : None

The header or list of header field names which can be used when this resource is accessed by allowed origins.

#### supports_credentials
> Default : False

Allows users to make authenticated requests. If true, injects the `Access-Control-Allow-Credentials` header in responses.

#### max_age
> Default : None

The maximum time for which this CORS request maybe cached. This value is set as the `Access-Control-Max-Age` header.

#### send_wildcard
> Default : True

If True, and the origins parameter is `*`, a wildcard `Access-Control-Allow-Origin` header is sent, rather than the request's `Origin` header.

#### always_send
> Default : True

If True, CORS headers are sent even if there is no `Origin` in the request's headers.

#### automatic_options
> Default : True

If True, CORS headers will be returned for OPTIONS requests. For use with cross domain POST requests which preflight OPTIONS requests, you will need to specifically allow the Content-Type header. ** Only applicable for use in the decorator**

#### vary_header
> Default : True

If True, the header Vary: Origin will be returned as per suggestion by the W3 implementation guidelines. Setting this header when the `Access-Control-Allow-Origin` is dynamically generated (e.g. when there is more than one allowed origin, and an Origin than '*' is returned) informs CDNs and other caches that the CORS headers are dynamic, and cannot be re-used. If False, the Vary header will never be injected or altered.

### Application-wide options

Alternatively, you can set all parameters **except automatic_options** in an app's config object. Setting these at the application level effectively changes the default value for your application, while still allowing you to override it on a per-resource basis, either via the CORS Flask-Extension and regular expressions, or via the `@cross_origin()` decorator.


The application-wide configuration options are identical to the keyword arguments to `cross_origin`, creatively prefixed with `CORS_`


* CORS_ORIGINS
* CORS_METHODS
* CORS_HEADERS
* CORS_EXPOSE_HEADERS
* CORS_ALWAYS_SEND
* CORS_MAX_AGE
* CORS_SEND_WILDCARD
* CORS_ALWAYS_SEND

### Using JSON with CORS

When using JSON cross origin, browsers will issue a pre-flight OPTIONS request for POST requests. In order for browsers to allow POST requests with a JSON content type, you must allow the Content-Type header. The simplest way to do this is to simply set the CORS_HEADERS configuration value on your application, e.g:

```python
app.config['CORS_HEADERS'] = 'Content-Type'
```


## Documentation

For a full list of options, please see the full [documentation](http://flask-cors.readthedocs.org/en/latest/)


## Tests

A simple set of tests is included in `test/`. To run, install nose, and simply invoke `nosetests` or `python setup.py test` to exercise the tests.

## Contributing

Questions, comments or improvements? Please create an issue on [Github](https://github.com/wcdolphin/flask-cors), tweet at [@wcdolphin](https://twitter.com/wcdolphin) or send me an email.

## Credits

This Flask extension is based upon the [Decorator for the HTTP Access Control](http://flask.pocoo.org/snippets/56/) written by Armin Ronacher.
