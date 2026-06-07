---
title: CORS (extension)
description: API reference for the flask_cors.CORS extension.
---

```python
from flask_cors import CORS

CORS(app, **options)
```

Initializes Cross Origin Resource Sharing for the application. The arguments are
identical to [`cross_origin`](/flask-cors/api/decorator/), with the addition of a
`resources` parameter. The `resources` parameter defines a series of regular
expressions for resource paths to match and, optionally, the associated options
to be applied to that particular resource.

The settings for CORS are determined in the following order:

1. Resource-level settings (e.g. when passed as a dictionary)
2. Keyword-argument settings
3. App-level configuration settings (e.g. `CORS_*`)
4. Default settings

:::note
Because it is possible for multiple regular expressions to match a resource path,
the regular expressions are first sorted by length, from longest to shortest, in
order to match the most specific expression. This lets you define a number of
specific resource options with a wildcard fallback for everything else.
:::

## Usage

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for all routes and origins
CORS(app)

# Or scope it to a set of resources, with per-resource options
CORS(app, resources={
    r"/api/*": {"origins": ["https://example.com"]},
})
```

The extension can also be initialized lazily via the application factory
pattern:

```python
cors = CORS()

def create_app():
    app = Flask(__name__)
    cors.init_app(app)
    return app
```

## Parameters

### `resources`

The series of regular expressions and (optionally) associated CORS options to be
applied to the given resource path.

- If a **dict**, its keys must be regular expressions and its values must be a
  dict of kwargs identical to the kwargs below.
- If a **list**, it is a list of regular expressions for which the app-wide
  configured options are applied.
- If a **string**, it is a single regular expression for which the app-wide
  configured options are applied.

**Default:** match all (`/*`) and apply app-level configuration.

### `origins`

The origin, or list of origins, to allow requests from. The origin(s) may be
regular expressions, case-sensitive strings, or else an asterisk.

:::note
Origins must include the scheme and the port (if not port 80), e.g.
`CORS(app, origins=["http://localhost:8000", "https://example.com"])`.
:::

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

### `allow_private_network`

If `True`, the response header `Access-Control-Allow-Private-Network` will be set
to `'true'` whenever the request header `Access-Control-Request-Private-Network`
has the value `'true'`. If `False`, it will be set to `'false'` under the same
condition.

If the request header `Access-Control-Request-Private-Network` is not present, or
has a value other than `'true'`, the response header is not set.

**Type:** `bool` &middot; **Default:** `True`
