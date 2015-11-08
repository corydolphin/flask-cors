# Change Log

## 2.1.2
Fixes package installation. Requirements.txt was not included in Manifest. 


## 2.1.1
Stop dynamically referecing logger.

Disable internal logging by default and reduce logging verbosity 

## 2.1.0
Adds support for Flask Blueprints. 

## 2.0.1
Fixes Issue #124 where only the first of multiple headers with the same name would be passed through.

## 2.0.0
**New Defaults**

1. New defaults allow all origins, all headers.

**Breaking Changes**

1. Removed always_send option.
1. Removed 'headers' option as a backwards-compatible alias for 'allowed_headers' to reduce confusion.

## 2.0.0rc1
Would love to get some feedback to make sure there are no unexpected regressions. This should be backwards compatible for most people.

Update default options and parameters in a backwards incompatible way.

By default, all headers are now allowed, and only requests with an
Origin header have CORS headers returned. If an Origin header is not
present, no CORS headers are returned.

Removed the following options: always_send, headers.

Extension and decorator are now in separate modules sharing a core module.
Test have been moved into the respective tests.extension and tests.decorator
modules. More work to decompose these tests is needed.


## 1.10.3
Release Version 1.10.3
* Adds logging to Flask-Cors so it is easy to see what is going on and why
* Adds support for compiled regexes as origins

Big thanks to @michalbachowski and @digitizdat!

## 1.10.2
This release fixes the behavior of Access-Control-Allow-Headers and Access-Control-Expose-Headers, which was previously swapped since 1.9.0.

To further fix the confusion, the `headers` parameter was renamed to more explicitly be `allow_headers`.

Thanks @maximium for the bug report and implementation!

## 1.10.1
This is a bug fix release, fixing:
Incorrect handling of resources and intercept_exceptions App Config options https://github.com/wcdolphin/flask-cors/issues/84
Issue with functools.partial in 1.10.0 using Python 2.7.9 https://github.com/wcdolphin/flask-cors/issues/83

Shoutout to @diiq and @joonathan for reporting these issues!

## 1.10.0
* Adds support for returning CORS headers with uncaught exceptions in production so 500s will have expected CORS headers set. This will allow clients to better surface the errors, rather than failing due to security. Reported and tested by @robertfw -- thanks!
* Improved conformance of preflight request handling to W3C spec.
* Code simplification and 100% test coverage :sunglasses:

## 1.9.0
* Improves API consistency, allowing a CORS resource of '*'
* Improves documentation of the CORS app extension
* Fixes test import errors on Python 3.4.1 (Thanks @wking )

## 1.8.1
Thanks to @wking's work in PR https://github.com/wcdolphin/flask-cors/pull/71 `python setup.py test` will now work.


## v1.8.0
Adds support for regular expressions in the list of origins.

This allows subdomain wildcarding and should be fully backwards compatible.

Credit to @marcoqu for opening https://github.com/wcdolphin/flask-cors/issues/54 which inspired this work

## Earlier
Prior version numbers were not kept track of in this system.
