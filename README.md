# Flask-CORS

[![Build Status](https://api.travis-ci.org/wcdolphin/flask-cors.png?branch=master)](https://travis-ci.org/wcdolphin/flask-cors)
[![Latest Version](https://pypip.in/version/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/)
[![Downloads](https://pypip.in/download/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/)
[![Supported Python versions](https://pypip.in/py_versions/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/)
[![License](https://pypip.in/license/Flask-Cors/badge.svg)](https://pypi.python.org/pypi/Flask-Cors/)

A Flask extension for handling Cross Origin Resource Sharing (CORS), making
cross-origin AJAX possible.


## Installation

Install the extension with using pip, or easy_install.
```bash
$ pip install flask-cors
```

## Usage
This extension exposes a simple decorator to decorate flask routes with. Simply
add `@cross_origin()` below a call to Flask's `@app.route(..)` incanation to
accept the default options and allow CORS on a given route.


### Simple Usage

```python
@app.route("/")
@cross_origin() # allow all origins all methods.
def helloWorld():
  return "Hello, cross-origin-world!"
```

### Using JSON with Cross Origin
When using JSON cross origin, browsers will issue a pre-flight OPTIONS request
for POST requests. In order for browsers to allow POST requests with a JSON
content type, you must allow the Content-Type header.

```python
@app.route("/user/create", methods=['GET','POST'])
@cross_origin(headers=['Content-Type']) # Send Access-Control-Allow-Headers
def cross_origin_json_post():
  return jsonify(success=True)
```


### Application-wide settings
Alternatively, you can set all but the 'automatic_options' parameter in an app's config
object. Setting these at the application level effectively changes the
default value for your application, while still allowing you to override
it on a per-resource basis.

The application-wide configuration options are creatively prefixed with CORS_
e.g.
* CORS_ORIGINS
* CORS_METHODS
* CORS_HEADERS
* CORS_EXPOSE_HEADERS
* CORS_ALWAYS_SEND
* CORS_MAX_AGE
* CORS_SEND_WILDCARD
* CORS_ALWAYS_SEND


For a full list of options, please see the full [documentation](http://flask-cors.readthedocs.org/en/latest/)


## Tests
A simple set of tests is included in `test/`. To run, install nose, and simply invoke `nosetests` or `python setup.py test` to exercise the tests.

## Contributing
Questions, comments or improvements? Please create an issue on [Github](https://github.com/wcdolphin/flask-cors), tweet at [@wcdolphin](https://twitter.com/wcdolphin) or send me an email.

