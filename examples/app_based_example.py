"""
Flask-Cors example
===================
This is a tiny Flask Application demonstrating Flask-Cors, making it simple
to add cross origin support to your flask app!

:copyright: (C) 2013 by Cory Dolphin.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, jsonify
try:
    # The typical way to import flask-cors
    from flask.ext.cors import CORS, cross_origin
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS, cross_origin

app = Flask(__name__)


# Set CORS options on app configuration
app.config['CORS_HEADERS'] = "Content-Type"
app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}

cors = CORS(app)

## Equivalent to (but using both is not advised)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}},
            headers="Content-Type")


@app.route("/")
def helloWorld():
    '''
        Since the path '/' does not match the regular expression r'/api/*',
        this route does not have CORS headers set.
    '''
    return '''This view is not exposed over CORS.'''


@app.route("/api/v1/users/")
def list_users():
    '''
        Since the path matches the regular expression r'/api/*', this resource
        automatically has CORS headers set. The expected result is as follows:

        $ http get http://127.0.0.1:5000/api/v1/users/
        HTTP/1.0 200 OK
        Access-Control-Allow-Headers: Content-Type
        Access-Control-Allow-Origin: *
        Content-Length: 21
        Content-Type: application/json
        Date: Sat, 09 Aug 2014 00:26:41 GMT
        Server: Werkzeug/0.9.4 Python/2.7.8

        {
            "success": true
        }

    '''
    return jsonify(success=True)


@app.route("/api/v1/users/create", methods=['POST'])
@cross_origin(origins="http://foo.com")
def create_user():
    '''
        This resource both matches the regular expression r'/api/*', and is
        also decorated with the cross_origin decorator. Since The decorator
        actually modifies the view function, and will run before the response
        is touched by the CORS object, the settings for CORS defined in the
        decorator will be used e.g. the allowed origin is only 'http://foo.com',
        rather than the more permissive '*' default.
        Thus, the expected headers are as follows:

        HTTP/1.0 200 OK
        Access-Control-Allow-Headers: Content-Type
        Access-Control-Allow-Origin: http://foo.com
        Content-Length: 21
        Content-Type: application/json
        Date: Sat, 09 Aug 2014 00:32:02 GMT
        Server: Werkzeug/0.9.4 Python/2.7.8
        Vary: Origin

        {
            "success": true
        }
    '''

    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True)
