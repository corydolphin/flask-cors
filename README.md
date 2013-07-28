# Flask-CORS

Flask-CORS is a simple extension to Flask allowing you to support
cross origin resource sharing (CORS) using a simple decorator.


## Installation

Install the extension with one of the following commands:

    $ easy_install flask-cors

or alternatively if you have pip installed (which you should):

    $ pip install flask-cors


## Usage

### Simple Usage

```
from flask import Flask
from flask.ext.cors import origin

app = Flask(__name__)
SECRET_KEY = "not actually a secret"
app.config.from_object(__name__)


@app.route("/")
@origin('*') # allow all origins all methods.
def helloWorld():
  return "hello world"

if __name__ == "__main__":
    app.run(debug=True)
```

### Options

*  `origin` a list of origins to support
*  `methods` a list or string of methods to support
*  `max_age` a timedelta or string to set Access-Control-Max-Age headers
*  `headers` Headers to set Access-Control-Allow-Headers