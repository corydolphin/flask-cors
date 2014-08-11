Flask-CORS
==========

| |Build Status|
| |Latest Version|
| |Downloads|
| |Supported Python versions|
| |License|

| A Flask extension for handling Cross Origin Resource Sharing (CORS),
making
| cross-origin AJAX possible.

Installation
------------

Install the extension with using pip, or easy\_install.

.. code:: bash

    $ pip install flask-cors

Usage
-----

This extension enables CORS support either via a decorator, or a Flask
extension. There are three examples shown in the
`examples <https://github.com/wcdolphin/flask-cors/tree/master/examples>`__
directory, showing the major use cases. The suggested configuration is
the
`simple\_example.py <https://github.com/wcdolphin/flask-cors/tree/master/examples/simple_example.py>`__,
or the
`app\_example.py <https://github.com/wcdolphin/flask-cors/tree/master/examples/app_based_example.py>`__.

Simple Usage
~~~~~~~~~~~~

In the simplest case, initialize the Flask-Cors extension with default
arguments in order to allow CORS on all routes.

.. code:: python


    app = Flask(__name__)
    cors = CORS(app)

    @app.route("/")
    def helloWorld():
      return "Hello, cross-origin-world!"

Resource specific CORS
^^^^^^^^^^^^^^^^^^^^^^

Alternatively, a list of resources and associated settings for CORS can
be supplied, selectively enables CORS support on a set of paths on your
app.

Note: this resources parameter can also be set in your application's
config.

.. code:: python

    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route("/api/v1/users")
    def list_users():
      return "user example"

Route specific CORS via decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This extension also exposes a simple decorator to decorate flask routes
with. Simply add ``@cross_origin()`` below a call to Flask's
``@app.route(..)`` incanation to accept the default options and allow
CORS on a given route.

.. code:: python

    @app.route("/")
    @cross_origin() # allow all origins all methods.
    def helloWorld():
      return "Hello, cross-origin-world!"

Using JSON with CORS
~~~~~~~~~~~~~~~~~~~~

| When using JSON cross origin, browsers will issue a pre-flight OPTIONS
request for POST requests. In order for browsers to allow POST requests
with a JSON content type, you must allow the Content-Type header. The
simplest way to do this is to simply set the CORS\_HEADERS configuration
value on your application:
| e.g.

.. code:: python

    app.config['CORS_HEADERS'] = 'Content-Type'

Application-wide settings
~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can set all parameters **except automatic\_options**
in an app's config object. Setting these at the application level
effectively changes the default value for your application, while still
allowing you to override it on a per-resource basis, either via the
CORSEnabler and regular expressions, or via the ``@cross_origin()``
decorator.

The application-wide configuration options are creatively prefixed with
'CORS\_' e.g.

-  CORS\_ORIGINS
-  CORS\_METHODS
-  CORS\_HEADERS
-  CORS\_EXPOSE\_HEADERS
-  CORS\_ALWAYS\_SEND
-  CORS\_MAX\_AGE
-  CORS\_SEND\_WILDCARD
-  CORS\_ALWAYS\_SEND

For a full list of options, please see the full
`documentation <http://flask-cors.readthedocs.org/en/latest/>`__

Tests
-----

A simple set of tests is included in ``test/``. To run, install nose,
and simply invoke ``nosetests`` or ``python setup.py test`` to exercise
the tests.

Contributing
------------

Questions, comments or improvements? Please create an issue on
`Github <https://github.com/wcdolphin/flask-cors>`__, tweet at
`@wcdolphin <https://twitter.com/wcdolphin>`__ or send me an email.

Credits
-------

This Flask extension is based upon the `Decorator for the HTTP Access
Control <http://flask.pocoo.org/snippets/56/>`__ written by Armin
Ronacher.

.. |Build Status| image:: https://api.travis-ci.org/wcdolphin/flask-cors.png?branch=master
   :target: https://travis-ci.org/wcdolphin/flask-cors
.. |Latest Version| image:: https://pypip.in/version/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
.. |Downloads| image:: https://pypip.in/download/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
.. |Supported Python versions| image:: https://pypip.in/py_versions/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
.. |License| image:: https://pypip.in/license/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
