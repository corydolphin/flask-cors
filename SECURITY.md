# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Flask-CORS, please report it
privately so it can be patched before public disclosure.

**Preferred channel: GitHub Security Advisories.**

Open a private advisory at:
<https://github.com/corydolphin/flask-cors/security/advisories/new>

This route is private to maintainers and lets us coordinate a fix and a
CVE assignment before any public discussion.

Please include, when possible:

- The Flask-CORS version affected (`pip show Flask-Cors`).
- A minimal Flask app reproducing the issue.
- The expected vs. observed behaviour, including any HTTP exchange.
- Your assessment of impact (e.g. origin bypass, header injection,
  privilege escalation).

If you cannot use GitHub Security Advisories, please email
`corydolphin@gmail.com` with the subject line `flask-cors security`.

## Supported Versions

Only the latest minor release line receives security fixes. Older
versions may be patched on a best-effort basis.

## Disclosure

Once a fix is available we will publish a GitHub Security Advisory,
request a CVE if appropriate, and credit the reporter (unless asked
otherwise).

## Past advisories

Past CVEs and fixes are listed under the project's
[Security tab](https://github.com/corydolphin/flask-cors/security)
and in the
[CHANGELOG](https://github.com/corydolphin/flask-cors/blob/main/CHANGELOG.md).
