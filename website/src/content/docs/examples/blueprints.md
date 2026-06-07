---
title: Using CORS with Blueprints
description: Flask-CORS supports blueprints out of the box.
---

Flask-CORS supports blueprints out of the box. Simply pass a `Blueprint` instance
to the CORS extension and everything will just work.

```python
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS

api_v1 = Blueprint("API_v1", __name__)

CORS(api_v1)  # enable CORS on the API_v1 blueprint


@api_v1.route("/api/v1/users/")
def list_users():
    return jsonify(user="joe")


@api_v1.route("/api/v1/users/create", methods=["POST"])
def create_user():
    return jsonify(success=True)


public_routes = Blueprint("public", __name__)


@public_routes.route("/")
def hello_world():
    # The path '/' is on a blueprint without CORS, so it has no CORS headers.
    return "<h1>Hello CORS!</h1>"


app = Flask("FlaskCorsBlueprintBasedExample")
app.register_blueprint(api_v1)
app.register_blueprint(public_routes)


if __name__ == "__main__":
    app.run(debug=True)
```

:::tip
The full, runnable version of this example lives in
[`examples/blueprints_based_example.py`](https://github.com/corydolphin/flask-cors/blob/main/examples/blueprints_based_example.py).
:::
