Flask-CORS
==========

Flask-CORS is a simple extension to Flask allowing you to support cross
origin resource sharing (CORS) using a simple decorator.

|Build Status|

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

Alternatively, setting your application's ``CORS_ORIGINS`` configuration
property will

.. code:: python

    app.config['CORS_ORIGINS'] = ['Foo', 'Bar']


    @app.route("/")
    @cross_origin() # will return CORS headers for origins 'Foo' and 'Bar'
    def helloWorld():
      return "Hello, cross-origin-world!"

For a full list of options, please see the full
`documentation <http://flask-cors.readthedocs.org/en/latest/>`__

Tests
-----

A simple set of tests is included in ``test.py``. To run, install nose,
and simply invoke ``nosetests`` or run ``python test.py`` or
``python setup.py test`` to exercise the tests.

Contributing
------------

Questions, comments or improvements? Please create an issue on
`Github <https://github.com/wcdolphin/flask-cors>`__, tweet at
[@wcdolphin](https://twitter.com/wcdolphin) or send me an email.

|Bitdeli Badge|

.. |Build Status| image:: https://travis-ci.org/wcdolphin/flask-cors.png?branch=master
   :target: https://travis-ci.org/wcdolphin/flask-cors
.. |Bitdeli Badge| image:: https://d2weczhvl823v0.cloudfront.net/wcdolphin/flask-cors/trend.png
   :target: https://bitdeli.com/free
