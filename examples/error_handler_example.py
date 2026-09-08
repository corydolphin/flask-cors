"""Allow a browser to read a missing route's JSON error after preflight."""

from flask import Flask

from flask_cors import cross_origin

app = Flask(__name__)


@app.errorhandler(404)
@cross_origin(origins=["https://client.example"], methods=["GET"], allow_headers=["X-Request-ID"])
def not_found(error):
    return {"error": "Not found"}, 404
