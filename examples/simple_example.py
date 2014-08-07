"""
Flask-Cors example
===================
This is a tiny Flask Application demonstrating Flask-Cors, making it simple
to add cross origin support to your flask app!

:copyright: (C) 2013 by Cory Dolphin.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, jsonify
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/api/*', headers='Content-Type')
# One of the simplest configurations. Exposes all resources to CORS
# and allows the Content-Type header, which is necessary to POST JSON
# cross origin.


@app.route("/")
def helloWorld():
    return '''<h1>Hello CORS!</h1> Read about my spec at the
<a href="http://www.w3.org/TR/cors/">W3</a> Or, checkout my documentation
on <a href="https://github.com/wcdolphin/flask-cors">Github</a>'''


@app.route("/api/v1/users/")
def list_users():
    return jsonify(success=True)


@app.route("/api/v1/users/create", methods=['POST'])
def create_user():
    return jsonify(success=True)



if __name__ == "__main__":
    app.run(debug=True)
