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

    $ pip install flask-cors

Usage
-----

This extension exposes a simple decorator to decorate flask routes with.
Simply add ``@cross_origin()`` below a call to Flask's
``@app.route(..)`` incanation to accept the default options and allow
CORS on a given route.

Simple Usage
~~~~~~~~~~~~

.. code:: python

    @app.route("/")
    @cross_origin() # allow all origins all methods.
    def helloWorld():
      return "Hello, cross-origin-world!"

Using JSON with Cross Origin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using JSON cross origin, browsers will issue a pre-flight OPTIONS
request for POST requests. In order for browsers to allow POST requests
with a JSON content type, you must allow the Content-Type header.

.. code:: python

    @app.route("/user/create", methods=['GET','POST'])
    @cross_origin(headers=['Content-Type']) # Send Access-Control-Allow-Headers
    def cross_origin_json_post():
      return jsonify(success=True)

Application-wide settings
~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can set any of these options in an app's config
object. Setting these at the application level effectively changes the
default value for your application, while still allowing you to override
it on a per-resource basis.

The application-wide configuration options are creatively prefixed with
CORS\_ e.g. \* CORS\_ORIGINS \* CORS\_METHODS \* CORS\_HEADERS \*
CORS\_EXPOSE\_HEADERS \* CORS\_ALWAYS\_SEND \* CORS\_MAX\_AGE \*
CORS\_SEND\_WILDCARD \* CORS\_ALWAYS\_SEND \* CORS\_AUTOMATIC\_OPTIONS

.. code:: python

    app.config['CORS_ORIGINS'] = ['https://foo.com', 'http://www.bar.com']
    app.config['CORS_HEADERS'] = ['Content-Type']

    # Will return CORS headers for origins 'https://foo.com'and 'http://www.bar.com'
    # and an Access-Control-Allow-Headers of 'Content-Type'
    """
    Will return CORS headers for origins 'https://foo.com'and
    'http://www.bar.com' and an Access-Control-Allow-Headers of 'Content-Type'
    E.G. Testing with httpie
        ➜  ~  http GET http://127.0.0.1:5000/
        HTTP/1.0 200 OK
        Access-Control-Allow-Headers: Content-Type
        Access-Control-Allow-Origin: https://foo.com, http://www.bar.com
        Content-Length: 26
        Content-Type: text/html; charset=utf-8
        Date: Tue, 22 Jul 2014 23:55:53 GMT
        Server: Werkzeug/0.9.4 Python/2.7.8

        Hello, cross-origin-world!
    """
    @app.route("/")
    @cross_origin()
    def helloWorld():
      return "Hello, cross-origin-world!"


    """
    Will return CORS headers for 'google.com' and  Access-Control-Allow-Headers of
    'Content-Type'.
    E.G. Testing with httpie
         ➜  ~  http GET http://127.0.0.1:5000/special
        HTTP/1.0 200 OK
        Access-Control-Allow-Headers: Content-Type
        Access-Control-Allow-Origin: http://google.com
        Content-Length: 33
        Content-Type: text/html; charset=utf-8
        Date: Tue, 22 Jul 2014 23:55:29 GMT
        Server: Werkzeug/0.9.4 Python/2.7.8

        Hello, google-cross-origin-world!
    """
    @app.route("/special")
    @cross_origin(origins="http://google.com")
    def helloGoogle():
      return "Hello, google-cross-origin-world!"

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
[@wcdolphin](https://twitter.com/wcdolphin) or send me an email.

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
