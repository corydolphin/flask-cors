# flask-cors

[![Release](https://img.shields.io/github/v/release/corydolphin/flask-cors)](https://img.shields.io/github/v/release/corydolphin/flask-cors)
[![Build status](https://img.shields.io/github/actions/workflow/status/corydolphin/flask-cors/main.yml?branch=main)](https://github.com/corydolphin/flask-cors/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/corydolphin/flask-cors)](https://img.shields.io/github/commit-activity/m/corydolphin/flask-cors)
[![License](https://img.shields.io/github/license/corydolphin/flask-cors)](https://img.shields.io/github/license/corydolphin/flask-cors)

A Flask extension for handling Cross Origin Resource Sharing (CORS),
making cross-origin AJAX possible.

This package has a simple philosophy: when you want to enable CORS, you
wish to enable it for all use cases on a domain. This means no mucking
around with different allowed headers, methods, etc.

By default, submission of cookies across domains is disabled due to the
security implications. Please see the documentation for how to enable
credential\'ed requests, and please make sure you add some sort of
[CSRF](http://en.wikipedia.org/wiki/Cross-site_request_forgery)
protection before doing so!

# Installation

Install the extension with using pip, uv, or your favorite package manager

```console
pip install -U flask-cors
```

# Getting Started

This package exposes a Flask extension which by default enables CORS support on all routes, for all origins and methods. It allows parameterization of all CORS headers on a per-resource level. The package also contains a decorator, for those who prefer this approach.

In the simplest case, initialize the Flask-Cors extension with default arguments in order to allow CORS for all domains on all routes. See the full list of options in the documentation.

```py hl_lines="2 5"
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

```

# Using CORS with Cookies

By default, Flask-CORS does not allow cookies to be submitted across sites, since it has potential security implications.
If you wish to enable cross-site cookies, you may wish to add some sort of [CSRF](http://en.wikipedia.org/wiki/Cross-site_request_forgery)
protection to keep you and your users safe.

To allow cookies or authenticated requests to be made cross origins, simply set the `supports_credentials` option to `True`. E.g.

```py hl_lines="2 5"
    from flask import Flask, session
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.route("/")
    def helloWorld():
      return "Hello, %s" % session['username']
```