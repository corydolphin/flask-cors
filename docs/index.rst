Flask-CORS
==========

A Flask extension for handling Cross Origin Resource Sharing (CORS),
making cross-origin AJAX possible.

Contact
-------

Questions, comments or improvements? Please create an issue on
`Github <https://github.com/wcdolphin/flask-cors>`__, tweet at
`@wcdolphin <https://twitter.com/wcdolphin>`__ or send me an email.

Flask-CORS
==========

|Build Status| |Latest Version| |Downloads| |Supported Python versions|
|License|

A Flask extension for handling Cross Origin Resource Sharing (CORS),
making cross-origin AJAX possible.

Installation
------------

Install the extension with using pip, or easy\_install.

.. code:: bash

    $ pip install -U flask-cors

Usage
-----

This extension enables CORS support either via a decorator, or a Flask
extension. This extension enables CORS support either via a decorator, or a Flask
extension. There are three examples shown in the examples directory, showing
the major use cases.

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

Alternatively, a list of resources and associated settings for CORS
can be supplied, selectively enables CORS support on a set of paths on your
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

This extension also exposes a simple decorator to decorate flask
routes with.
Simply add ``@cross_origin()`` below a call to Flask's
``@app.route(..)``
incanation to accept the default options and allow CORS on a given
route.

.. code:: python

    @app.route("/")
    @cross_origin() # allow all origins all methods.
    def helloWorld():
      return "Hello, cross-origin-world!"

Using JSON with CORS
~~~~~~~~~~~~~~~~~~~~

When using JSON cross origin, browsers will issue a pre-flight OPTIONS
request for POST requests. In order for browsers to allow POST requests with a
JSON content type, you must allow the Content-Type header. The simplest way
to do this is to simply set the CORS\_HEADERS configuration value on your
application:
e.g.

.. code:: python

    app.config['CORS_HEADERS'] = 'Content-Type'



Full description of options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: flask_cors.cross_origin


More examples
~~~~~~~~~~~~~

A simple, and suggested example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the suggested approach to enabling CORS. The default configuration
will work well for most use cases.

.. literalinclude:: ../examples/simple_example.py
   :language: python

A more complicated example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you require advanced configuration and more specific configuration of CORS
support for your application, this example provides a useful example of
multiple regular expressions and options.

.. literalinclude:: ../examples/app_based_example.py
   :language: python

A view-based example
~~~~~~~~~~~~~~~~~~~~~
Alternatively, using the decorator on a per view basis enables CORS for only
a particular view.

.. literalinclude:: ../examples/view_based_example.py
   :language: python


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


