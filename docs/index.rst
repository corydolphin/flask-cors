.. Flask-Cors documentation master file, created by
   sphinx-quickstart on Thu Dec 19 13:46:50 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

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

.. |Build Status| image:: https://travis-ci.org/wcdolphin/flask-cors.png?branch=master
   :target: https://travis-ci.org/wcdolphin/flask-cors


Options
~~~~~~~

.. autofunction:: flask_cors.cross_origin

