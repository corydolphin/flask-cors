---
title: cross_origin (decorator)
description: API reference for the flask_cors.cross_origin decorator.
---

```python
from flask_cors import cross_origin

@cross_origin(**options)
```

This is the decorator used to wrap a Flask route. In the simplest case, use the
default parameters to allow all origins — the most permissive configuration.

:::caution
If the decorated view modifies state or performs authentication which may be
brute-forced, you should add some degree of protection, such as Cross Site
Request Forgery (CSRF) protection.
:::

## Usage

```python
from flask import Flask
from flask_cors import cross_origin

app = Flask(__name__)

@app.route("/")
@cross_origin()
def hello_world():
    return "Hello, cross-origin-world!"
```

Apply options to scope what a single view allows:

```python
@app.route("/api/items", methods=["POST"])
@cross_origin(origins="https://example.com", allow_headers=["Content-Type"])
def create_item():
    ...
```

## Parameters

### `origins`

The origin, or list of origins, to allow requests from. The origin(s) may be
regular expressions, case-sensitive strings, or else an asterisk.

**Type:** `list`, `string`, or `regex` &middot; **Default:** `'*'`

### `methods`

The method or list of methods which the allowed origins are allowed to access for
non-simple requests.

**Type:** `list` or `string` &middot; **Default:** `[GET, HEAD, POST, OPTIONS, PUT, PATCH, DELETE]`

### `expose_headers`

The header or list of headers which are safe to expose to the API of a CORS API
specification.

**Type:** `list` or `string` &middot; **Default:** `None`

### `allow_headers`

The header or list of header field names which can be used when this resource is
accessed by allowed origins. The header(s) may be regular expressions,
case-sensitive strings, or else an asterisk.

**Type:** `list`, `string`, or `regex` &middot; **Default:** `'*'` (allow all headers)

### `supports_credentials`

Allows users to make authenticated requests. If `True`, injects the
`Access-Control-Allow-Credentials` header in responses. This allows cookies and
credentials to be submitted across domains.

:::caution
This option cannot be used in conjunction with a `'*'` origin.
:::

**Type:** `bool` &middot; **Default:** `False`

### `max_age`

The maximum time for which this CORS request may be cached. This value is set as
the `Access-Control-Max-Age` header.

**Type:** `timedelta`, `integer`, `string`, or `None` &middot; **Default:** `None`

### `send_wildcard`

If `True`, and the `origins` parameter is `*`, a wildcard
`Access-Control-Allow-Origin` header is sent rather than echoing the request's
`Origin` header.

**Type:** `bool` &middot; **Default:** `False`

### `vary_header`

If `True`, the header `Vary: Origin` will be returned as per the W3
implementation guidelines.

Setting this header when the `Access-Control-Allow-Origin` is dynamically
generated (e.g. when there is more than one allowed origin, and an origin other
than `*` is returned) informs CDNs and other caches that the CORS headers are
dynamic and cannot be cached. If `False`, the `Vary` header will never be
injected or altered.

**Type:** `bool` &middot; **Default:** `True`

### `automatic_options`

Only applies to the `cross_origin` decorator. If `True`, Flask-CORS will override
Flask's default OPTIONS handling to return CORS headers for OPTIONS requests.

**Type:** `bool` &middot; **Default:** `True`
