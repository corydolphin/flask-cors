"""
Flask-Cors example
===================
This is a tiny Flask Application demonstrating Flask-Cors, makign it simple
to add cross origin support to your flask app!

:copyright: (C) 2013 by Cory Dolphin.
:license:   MIT/X11, see LICENSE for more details.
"""
from flask import Flask

try:
  import flask_cors.origin # support local usage without installed package
except:
  from flask.ext.cors import origin # this is how you would normally import

app = Flask(__name__)
SECRET_KEY = "yeah, not actually a secret"
app.config.from_object(__name__)


@app.route("/")
@origin('*')
def helloWorld():
  return "hello world"

if __name__ == "__main__":
    app.run(debug=True)
