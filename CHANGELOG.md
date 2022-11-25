# Change Log

## 3.0.10
Adds support for PPC64 and ARM64 builds for distribution. Thanks @sreekanth370

## 3.0.9
### Security
 - Escape path before evaluating resource rules (thanks to Colby Morgan). Prior to this, flask-cors incorrectly
 evaluated CORS resource matching before path expansion. E.g. "/api/../foo.txt" would incorrectly match resources for
 "/api/*" whereas the path actually expands simply to "/foo.txt"

## 3.0.8
Fixes : DeprecationWarning: Using or importing the ABCs from 'collections' in Python 3.7.
Thank you @juanmaneo and @jdevera for the contribution.

## 3.0.7
Updated logging.warn to logging.warning (#234) Thanks Vaibhav

## 3.0.6
Manual error in release process. Identical contents at 3.0.5. 

## 3.0.5
Fixes incorrect handling of regexes containing `[`, and a few other special characters. Fixes Issue [#212](https://github.com/corydolphin/flask-cors/issues/212) 

## 3.0.4
Handle response.headers being None. (Fixes issue #217)

## 3.0.3
Ensure that an Origin of '*' is never sent if supports_credentials is True (fixes Issue #202)
* If `always_send=True`, and `'*'` is in the allowed origins, and a request is made without an Origin header, no `Access-Control-Allow-Origins` header will now be returned. This is breaking if you depended on it, but was a bug as it goes against the spec.

## 3.0.2
Fixes Issue #187: regression whereby header (and domain) matching was incorrectly case sensitive. Now it is not, making the behavior identical to 2.X and 1.X.

## 3.0.1
Fixes Issue #183: regression whereby regular expressions for origins with an "?" are not properly matched.

## 3.0.0

This release is largely a number of small bug fixes and improvements, along with a default change in behavior, which is technically a breaking change.

**Breaking Change**
We added an always_send option, enabled by default, which makes Flask-CORS inject headers even if the request did not have an 'Origin' header. Because this makes debugging far easier, and has very little downside, it has also been set as the default, making it technically a breaking change. If this actually broke something for you, please let me know, and I'll help you work around it. (#156) c7a1ecdad375a796155da6aca6a1f750337175f3


Other improvements:
* Adds building of universal wheels (#175) 4674c3d54260f8897bd18e5502509363dcd0d0da
* Makes Flask-CORS compatible with OAuthLib's custom header class ... (#172) aaaf904845997a3b684bc6677bdfc91656a85a04
* Fixes incorrect substring matches when strings are used as origins or headers (#165) 9cd3f295bd6b0ba87cc5f2afaca01b91ff43e72c
* Fixes logging when unknown options are supplied (#152) bddb13ca6636c5d559ec67a95309c9607a3fcaba


## 2.1.3
Fixes Vary:Origin header sending behavior when regex origins are used.


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
