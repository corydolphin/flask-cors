# Flask-CORS

Flask-CORS is a simple extension to Flask allowing you to support
cross origin resource sharing (CORS) using a simple decorator.

[![Build Status](https://travis-ci.org/wcdolphin/flask-cors.png?branch=master)](https://travis-ci.org/wcdolphin/flask-cors)

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
Alternatively, setting your application's `CORS_ORIGINS` or `CORS_HEADERS`
configuration property will effectively change the default value for your
application, while still allowing you to override it on a per-resource basis:

```python
app.config['CORS_ORIGINS'] = ['https://foo.com', 'http://www.bar.com']
app.config['CORS_HEADERS'] = ['Content-Type']

# Will return CORS headers for origins 'https://foo.com'and 'http://www.bar.com'
# and an Access-Control-Allow-Headers of 'Content-Type'
"""
Will return CORS headers for origins 'https://foo.com'and
'http://www.bar.com' and an Access-Control-Allow-Headers of 'Content-Type'
E.G. Testing with httpie
    ➜  ~  http GET http://127.0.0.1:5000/
    HTTP/1.0 200 OK
    Access-Control-Allow-Headers: Content-Type
    Access-Control-Allow-Origin: https://foo.com, http://www.bar.com
    Content-Length: 26
    Content-Type: text/html; charset=utf-8
    Date: Tue, 22 Jul 2014 23:55:53 GMT
    Server: Werkzeug/0.9.4 Python/2.7.8

    Hello, cross-origin-world!
"""
@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"


"""
Will return CORS headers for 'google.com' and  Access-Control-Allow-Headers of
'Content-Type'.
E.G. Testing with httpie
     ➜  ~  http GET http://127.0.0.1:5000/special
    HTTP/1.0 200 OK
    Access-Control-Allow-Headers: Content-Type
    Access-Control-Allow-Origin: http://google.com
    Content-Length: 33
    Content-Type: text/html; charset=utf-8
    Date: Tue, 22 Jul 2014 23:55:29 GMT
    Server: Werkzeug/0.9.4 Python/2.7.8

    Hello, google-cross-origin-world!
"""
@app.route("/special")
@cross_origin(origins="http://google.com")
def helloGoogle():
  return "Hello, google-cross-origin-world!"

```



For a full list of options, please see the full [documentation](http://flask-cors.readthedocs.org/en/latest/)


## Tests
A simple set of tests is included in `test.py`. To run, install nose, and simply invoke `nosetests` or run `python test.py` or `python setup.py test` to exercise the tests.

## Contributing
Questions, comments or improvements? Please create an issue on [Github](https://github.com/wcdolphin/flask-cors), tweet at [@wcdolphin](https://twitter.com/wcdolphin) or send me an email.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/wcdolphin/flask-cors/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

