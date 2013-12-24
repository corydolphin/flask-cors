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

For a full list of options, please see the full [documentation](http://flask-cors.readthedocs.org/en/latest/)


## Tests
A simple set of tests is included in `test.py`. To run, install nose, and simply invoke `nosetests` or run `python test.py` to exercise the tests. 

## Contributing
Questions, comments or improvements? Please create an issue on Github, tweet at me or send me an email.
