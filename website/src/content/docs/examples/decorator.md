---
title: Using a view decorator
description: Isolate CORS to a small subset of views with the cross_origin decorator.
---

Flask-CORS can be used as a decorator on views, which makes it easy to isolate it
to a small subset of views.

```python
from flask import Flask, jsonify
from flask_cors import cross_origin

app = Flask("FlaskCorsViewBasedExample")


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    # This view has CORS enabled for all domains, representing the simplest
    # configuration of view-based decoration.
    return "<h1>Hello CORS!</h1>"


@app.route("/api/v1/users/create", methods=["GET", "POST"])
@cross_origin(allow_headers=["Content-Type"])
def cross_origin_json_post():
    # This view has CORS enabled for all domains, and allows browsers to send
    # the Content-Type header, allowing cross-domain AJAX POST requests.
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
```

:::tip
The full, runnable version of this example lives in
[`examples/view_based_example.py`](https://github.com/corydolphin/flask-cors/blob/main/examples/view_based_example.py).
:::
