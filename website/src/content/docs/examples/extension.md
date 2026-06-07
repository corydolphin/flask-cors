---
title: Using the extension
description: Centralized CORS configuration of resources by pattern using the CORS extension.
---

Flask-CORS can be used as an extension to provide centralized configuration of
resources by pattern.

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask("FlaskCorsAppBasedExample")

# One of the simplest configurations. Exposes all resources matching /api/* to
# CORS and allows the Content-Type header, which is necessary to POST JSON
# cross origin.
CORS(app, resources=r"/api/*")


@app.route("/")
def hello_world():
    # Since the path '/' does not match the regular expression r'/api/*',
    # this route does not have CORS headers set.
    return "<h1>Hello CORS!</h1>"


@app.route("/api/v1/users/")
def list_users():
    # Since the path matches r'/api/*', this resource automatically has CORS
    # headers set.
    return jsonify(user="joe")


@app.route("/api/v1/users/create", methods=["POST"])
def create_user():
    # Browsers will first make a preflight request to verify that the resource
    # allows cross-origin POSTs with a JSON Content-Type.
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
```

:::tip
The full, runnable version of this example lives in
[`examples/app_based_example.py`](https://github.com/corydolphin/flask-cors/blob/main/examples/app_based_example.py).
:::
