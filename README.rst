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
extension. There are three examples shown in the
`examples <https://github.com/corydolphin/flask-cors/tree/master/examples>`__
directory, showing the major use cases. The suggested configuration is
the
`app\_based\_example.py <https://github.com/corydolphin/flask-cors/blob/master/examples/app_based_example.py>`__,
or the
`view\_based\_example.py <https://github.com/corydolphin/flask-cors/blob/master/examples/view_based_example.py>`__.
A full list of options can be found in the
`documentation <http://flask-cors.readthedocs.org/en/latest/>`__.

This package has a simple philosophy, when you want to enable CORS, you
wish to enable it for all use cases on a domain. This means no mucking
around with different allowed headers, methods, etc. By default,
submission of cookies across domains is disabled due to the security
implications, please see the documentation for how to enable
credential'ed requests, and please make sure you add some sort of
`CRSF <http://en.wikipedia.org/wiki/Cross-site_request_forgery>`__
protection before doing so!

Simple Usage
~~~~~~~~~~~~

In the simplest case, initialize the Flask-Cors extension with default
arguments in order to allow CORS for all domains on all routes.

.. code:: python


    from flask import Flask
    from flask.ext.cors import CORS

    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def helloWorld():
      return "Hello, cross-origin-world!"

Initializing the extension with a blueprint is also feasible:

.. code:: python


    from flask import Flask, Blueprint
    from flask.ext.cors import CORS

    blueprint = Blueprint('myblueprint', __name__)
    CORS(blueprint)

    @blueprint.route("/")
    def helloBlueprints():
        return "Hello, cross-origin-world! Sincerely, a Flask Blueprint"

    app = Flask(__name__)
    app.register_blueprint(blueprint)

Resource specific CORS
^^^^^^^^^^^^^^^^^^^^^^

Alternatively, you can specify CORS options on a resource and origin
level of granularity by passing a dictionary as the 'resources' option,
mapping paths to a set of options.

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
``@app.route(..)`` to allow CORS on a given route.

.. code:: python

    @app.route("/")
    @cross_origin()
    def helloWorld():
      return "Hello, cross-origin-world!"

Logging
^^^^^^^

Flask-Cors uses standard Python logging, using the logger name
'``app.logger_name``.cors'. The app's logger name attribute is usually
the same as the name of the app. You can read more about logging from
`Flask's
documentation <http://flask.pocoo.org/docs/0.10/errorhandling/>`__.

.. code:: python

    import logging
    # make your awesome app
    logging.basicConfig(level=logging.INFO)

Documentation
-------------

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
`Github <https://github.com/corydolphin/flask-cors>`__, tweet at
`@corydolphin <https://twitter.com/corydolphin>`__ or send me an email.
I do my best to include every contribution proposed in any way that I
can.

Credits
-------

This Flask extension is based upon the `Decorator for the HTTP Access
Control <http://flask.pocoo.org/snippets/56/>`__ written by Armin
Ronacher.

.. |Build Status| image:: https://api.travis-ci.org/corydolphin/flask-cors.svg?branch=master
   :target: https://travis-ci.org/corydolphin/flask-cors
.. |Latest Version| image:: https://pypip.in/version/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
.. |Downloads| image:: https://pypip.in/download/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
.. |Supported Python versions| image:: https://pypip.in/py_versions/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
.. |License| image:: https://pypip.in/license/Flask-Cors/badge.svg
   :target: https://pypi.python.org/pypi/Flask-Cors/
