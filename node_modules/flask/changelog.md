# Flask Changelog

0.2.10 (11 May 2016)
-----------------
- Add the option to select specific fonts when defining font aliases.
  - Font aliases were previously limited to aliasing regular font variants.
- Add font-family mixin.
- Improve documentation and general test consistency and coverage.

0.2.9 (7 Jan 2016)
------------------
- Update various functions and mixins to use `font-family`.

0.2.8 (7 Jan 2016)
------------------
- Add `font-family` function.
- Add deprecation warning to `font-stack` function.
- Allow palette aliases to select non-base colors.
- Update npm dependencies.
- Add changelog.

0.2.7 (14 Sep 2015)
-------------------
- Fix `flask-is-testing` causing errors if not defined.

0.2.6 (14 Sep 2015)
------------------
- Flesh out documentation.
- Clean up test setup files.
- Move debug functions to Flask core.
- Add `flask-error` function to enable testing for sass errors.
- Make `$font-aliases` optional, return false instead of error.

0.2.5 (5 Aug 2015)
------------------
- Add `font-family-key` function and refactor `font-fallback` function.

0.2.4 (23 Jul 2015)
------------------
- Add `font-fallback` function.
- Revise fallback definition structure.
- Fix font reference string.
- Improve error reporting in font-name function.
- Use Mocha for running tests.

0.2.3 (21 Jul 2015)
------------------
- Update readme.
- Unify variable names by removing 'font-' prefix, set default variant of font mixin to use 'regular' like font-name and font-stack functions.

0.2.2 (15 Jun 2015)
------------------
- Revise testing file structure.

0.2.1 (12 Jun 2015)
------------------
- Fix typo in bower.json.

0.2.0 (12 Jun 2015)
------------------
- Add testing suite.
- Add the following font management functions and mixins:
    + `font-feature-settings` mixin
    + `font-modifiers` mixin
    + `font-name` function
    + `font-stack` function
    + `font-type` function
    + `font` mixin

0.1.1 (30 Apr 2015)
------------------
- Add Travis CI build status shield to readme.
- Enable palette warning.
- Add testing with True and Travis config.
- Revise sass folder structure.
- Add Sache support.
- Add contributor information.

0.1.0 (28 Apr 2015)
------------------
- Initial release.
- Add `palette()` function.
