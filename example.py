"""
Flask-Cors example
===================
This is a tiny Flask Application demonstrating Flask-Cors, makign it simple
to add cross origin support to your flask app!

:copyright: (C) 2013 by Cory Dolphin.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask, request, jsonify

try:
    # this is how you would normally import
    from flask.ext.cors import cross_origin
except:
    # support local usage without installed package
    from flask_cors import cross_origin

app = Flask(__name__)


@app.route("/", methods=['GET', 'OPTIONS'])
@cross_origin()
def helloWorld():
    return '''<h1>Hello CORS!</h1> Read about my spec at the
<a href="http://www.w3.org/TR/cors/">W3</a> Or, checkout my documentation
on <a href="https://github.com/wcdolphin/flask-cors">Github</a>'''


@app.route("/user/create", methods=['GET','POST'])
@cross_origin(headers=['Content-Type'], send_wildcard=False) # Send Access-Control-Allow-Headers
def cross_origin_json_post():
  return jsonify(success=True)


@app.route("/wild")
def all():
    return "foo"

if __name__ == "__main__":
    # FlaskCorsApp(app)
    app.run(debug=True)
