# Using CORS with a view decorator

Flask-CORS can be used as a decorator on views, which makes it easy to isolate it to a small subset of views.

```py
--8<-- "examples/view_based_example.py"
```
# Reading errors after a preflight request

For an unknown URL, Flask normally returns 404 to both `OPTIONS` and the actual
request. A browser requires a successful preflight response before sending the
actual request, so it may report a CORS failure without exposing the 404 body to
JavaScript. Adding CORS headers to the 404 preflight alone does not make it succeed.

If your application needs clients to read these errors, apply `cross_origin` to
the application's 404 handler. Keep `automatic_options=True` (the default): the
decorator answers `OPTIONS` with 200, while the handler still returns 404 for the
actual request. Place `@app.errorhandler` above `@cross_origin` so Flask registers
the decorated handler. Configure the origin, methods, and headers for your API:

```py
--8<-- "examples/error_handler_example.py"
```

For example, a `GET /missing` with an `X-Request-ID` header from
`https://client.example` can now complete preflight and expose the JSON 404 response.
This is an application-level handler for all missing routes; choose its CORS
policy accordingly. A successful preflight does not make the requested URL exist.
