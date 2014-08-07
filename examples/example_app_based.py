"""
Flask-Cors example
===================
This is a tiny Flask Application demonstrating Flask-Cors, making it simple
to add cross origin support to your flask app!

:copyright: (C) 2013 by Cory Dolphin.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, jsonify


from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)


# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}

cors = CORS(app)

## Equivalent to (but using both is not advised)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}},
            headers="Content-Type")


# This route is not exposed over CORS since the regexp /api/* does not match
@app.route("/")
def helloWorld():
    return '''This view is not exposed over CORS.'''


# This route is exposed over CORS since the regexp /api/* does match.
# The CORS_HEADER option is inherited from the app-wide configuration, thus
# the returned headers are as follows:
#
# Access-Control-Allow-Headers: Content-Type
# Access-Control-Allow-Origin: *
@app.route("/api/v1/users/")
def list_users():
    return jsonify(success=True)


# This route is exposed over CORS since the regexp /api/* does match.
@app.route("/api/v1/users/create", methods=['POST'])
@cross_origin(origins="http://foo.com")
def create_user():
    return jsonify(success=True)



if __name__ == "__main__":
    app.run(debug=True)
