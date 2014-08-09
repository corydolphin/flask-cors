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
    from flask.ext.cors import cross_origin
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import cross_origin


app = Flask(__name__)


@app.route("/", methods=['GET'])
@cross_origin()
def helloWorld():
    '''
        This view has CORS enabled for all domains, representing the simplest
        configuration of view-based decoration. The expected result is as
        follows:

        $ http get http://127.0.0.1:5000/
        HTTP/1.0 200 OK
        Access-Control-Allow-Origin: *
        Content-Length: 184
        Content-Type: text/html; charset=utf-8
        Date: Sat, 09 Aug 2014 00:35:39 GMT
        Server: Werkzeug/0.9.4 Python/2.7.8

        <h1>Hello CORS!</h1> Read about my spec at the
        <a href="http://www.w3.org/TR/cors/">W3</a> Or, checkout my
        documentation on <a href="https://github.com/wcdolphin/flask-cors">
        Github</a>

    '''
    return '''<h1>Hello CORS!</h1> Read about my spec at the
<a href="http://www.w3.org/TR/cors/">W3</a> Or, checkout my documentation
on <a href="https://github.com/wcdolphin/flask-cors">Github</a>'''


@app.route("/user/create", methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type'])
def cross_origin_json_post():
    '''
        This view has CORS enabled for all domains, and allows browsers
        to send the Content-Type header, allowing cross domain AJAX POST
        requests.

        $ http post http://127.0.0.1:5000/user/create
        HTTP/1.0 200 OK
        Access-Control-Allow-Headers: Content-Type
        Access-Control-Allow-Origin: *
        Content-Length: 21
        Content-Type: application/json
        Date: Sat, 09 Aug 2014 00:38:47 GMT
        Server: Werkzeug/0.9.4 Python/2.7.8

        {
            "success": true
        }

    '''

    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
