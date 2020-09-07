Configuration
=============

Flask-CORS can be configured at four different locations.
Configuration values are determined in the following order:

   #. Resource level settings (e.g when passed as a dictionary)
   #. Keyword argument settings
   #. App level configuration settings (e.g. CORS_*)
   #. :ref:`Default settings <cors_default_values>`

See :ref:`below <locations>` for more information.

Configuration options
~~~~~~~~~~~~~~~~~~~~~

Configuration options are consistently named across the various :ref:`locations <locations>` where they can be set.
A configuration option called *example* can be set with the resource dictionary key *example*, as the keyword argument *example* or as the Flask app configuration key *CORS_EXAMPLE*.

The configuration options recognised by Flask-CORS are:

CORS_ALLOW_HEADERS (:py:class:`~typing.List` or :py:class:`str`)
   Headers to accept from the client.
   Headers in the :http:header:`Access-Control-Request-Headers` request header (usually part of the preflight OPTIONS request) maching headers in this list will be included in the :http:header:`Access-Control-Allow-Headers` response header.

CORS_ALWAYS_SEND (:py:class:`bool`)
   Usually, if a request doesn't include an :http:header:`Origin` header, the client did not request CORS.
   This means we can ignore this request.

   However, if this is true, a most-likely-to-be-correct value is still set.

CORS_AUTOMATIC_OPTIONS (:py:class:`bool`)
   Only applies to the :py:meth:`flask_cors.cross_origin` decorator.
   If True, Flask-CORS will override Flask’s default OPTIONS handling to return CORS headers for OPTIONS requests.

CORS_EXPOSE_HEADERS (:py:class:`~typing.List` or :py:class:`str`)
   The CORS spec requires the server to give explicit permissions for the client to read headers in CORS responses (via the :http:header:`Access-Control-Expose-Headers` header).
   This specifies the headers to include in this header.

CORS_INTERCEPT_EXCEPTIONS (:py:class:`bool`)
   Whether to deal with Flask exception handlers or leave them alone (with respect to CORS headers).

CORS_MAX_AGE (:py:class:`~datetime.timedelta`, :py:class:`int` or :py:class:`str`)
   The maximum time for which this CORS request may be cached. 
   This value is set as the :http:header:`Access-Control-Max-Age` header.

CORS_METHODS (:py:class:`~typing.List` or :py:class:`str`)
   The method(s) which the allowed origins are allowed to access.
   These are included in the :http:header:`Access-Control-Allow-Methods` response headers to the preflight OPTIONS requests.
   
.. _cors_origins_setting:

CORS_ORIGINS (:py:class:`~typing.List`, :py:class:`str` or :py:class:`re.Pattern`)
   The origin(s) to allow requests from.
   An origin configured here that matches the value of the :http:header:`Origin` header in a preflight OPTIONS request is returned as the value of the :http:header:`Access-Control-Allow-Origin` response header.

CORS_RESOURCES (:py:class:`~typing.Dict`, :py:class:`~typing.List` or :py:class:`str`)
   The series of regular expression and (optionally) associated CORS options to be applied to the given resource path.                       
   
   If the value is a dictionary, it's keys must be regular expressions matching resources, and the values must be another dictionary of configuration options, as described in this section.
   
   If the argument is a list, it is expected to be a list of regular expressions matching resources for which the app-wide configured options are applied.     
   
   If the argument is a string, it is expected to be a regular expression matching resources for which the app-wide configured options are applied.        

CORS_SEND_WILDCARD (:py:class:`bool`)
   If :ref:`CORS_ORIGINS <cors_origins_setting>` is ``"*"`` and this is true, then the :http:header:`Access-Control-Allow-Origin` response header's value with be ``"*"`` as well, instead of the value of the :http:header:`Origin` request header.

CORS_SUPPORTS_CREDENTIALS (:py:class:`bool`)
   Allows users to make authenticated requests. 
   If true, injects the :http:header:`Access-Control-Allow-Credentials` header in responses. 
   This allows cookies and credentials to be submitted across domains.                 
   
   :note: This option cannot be used in conjunction with a "*" origin  

CORS_VARY_HEADER: (:py:class:`bool`)
   Enables or disables the injection of the :http:header:`Vary` response header is set to ``Origin``.
   This informs clients that our CORS headers are dynamic and cannot be cached.

.. _cors_default_values:

Default values
~~~~~~~~~~~~~~

* CORS_ALLOW_HEADERS: "*"
* CORS_ALWAYS_SEND: True
* CORS_AUTOMATIC_OPTIONS: True
* CORS_EXPOSE_HEADERS: None
* CORS_INTERCEPT_EXCEPTIONS: True
* CORS_MAX_AGE: None
* CORS_METHODS: [":http:method:`get`", ":http:method:`head`", ":http:method:`post`", ":http:method:`options`", ":http:method:`put`", ":http:method:`patch`", ":http:method:`delete`"]
* CORS_ORIGINS: "*"
* CORS_RESOURCES: r"/\*"
* CORS_SEND_WILDCARD: False
* CORS_SUPPORTS_CREDENTIALS: False
* CORS_VARY_HEADER: True

.. _locations:

Locations
~~~~~~~~~

Resource level settings
^^^^^^^^^^^^^^^^^^^^^^^

You can specify CORS options on a resource level of granularity by passing a dictionary as the *resources* keyword argument when instantiating the :py:class:`flask_cors.CORS` object (or when calling ``init_app`` on it), mapping paths to a set of options.

Keyword argument settings
^^^^^^^^^^^^^^^^^^^^^^^^^

For options matching all resources, it's also possible to simply set the configuration options using keyword arguments when instantiating the :py:class:`flask_cors.CORS` object (or when calling ``init_app`` on it).

App level configuration settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's good practice to keep your application configuration settings in one place.
This is also possible with Flask-CORS using the same configuration options in the Flas application's config object.

Default settings
^^^^^^^^^^^^^^^^

Finally, every setting has a :ref:`default value <cors_default_values>` as well.
