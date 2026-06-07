---
title: Getting Started
description: Install Flask-CORS and enable cross-origin requests on your Flask app.
---

This package exposes a Flask extension which by default enables CORS support on
all routes, for all origins and methods. It allows parameterization of all CORS
headers on a per-resource level. The package also contains a decorator, for
those who prefer this approach.

## Installation

Install the extension with pip, [uv](https://docs.astral.sh/uv/), or your
favorite package manager:

```sh
pip install -U flask-cors
```

## Enabling CORS

In the simplest case, initialize the Flask-CORS extension with default arguments
in order to allow CORS for all domains on all routes. See the
[API reference](/flask-cors/api/extension/) for the full list of options.

```python {2,5}
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def helloWorld():
    return "Hello, cross-origin-world!"
```

## Using CORS with Cookies

By default, Flask-CORS does not allow cookies to be submitted across sites, since
it has potential security implications. If you wish to enable cross-site cookies,
you may want to add some sort of
[CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery) protection to
keep you and your users safe.

To allow cookies or authenticated requests to be made cross-origin, set the
`supports_credentials` option to `True`:

```python {2,5}
from flask import Flask, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/")
def helloWorld():
    return "Hello, %s" % session["username"]
```

:::caution
`supports_credentials` cannot be used together with a wildcard (`*`) origin. When
credentials are enabled you must specify the exact origins you trust.
:::
