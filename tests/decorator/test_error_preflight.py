from examples.error_handler_example import app


def test_missing_route_preflight_and_error_response():
    client = app.test_client()
    response = client.options(
        "/missing",
        headers={
            "Origin": "https://client.example",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Request-ID",
        },
    )
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "https://client.example"
    assert response.headers["Access-Control-Allow-Methods"] == "GET"
    assert response.headers["Access-Control-Allow-Headers"] == "X-Request-ID"

    response = client.get("/missing", headers={"Origin": "https://client.example", "X-Request-ID": "123"})
    assert response.status_code == 404
    assert response.json == {"error": "Not found"}
    assert response.headers["Access-Control-Allow-Origin"] == "https://client.example"
    assert client.get("/missing").status_code == 404


def test_error_handler_rejects_other_origins_and_methods():
    client = app.test_client()
    for method in (client.get, client.options):
        response = method("/missing", headers={"Origin": "https://other.example"})
        assert "Access-Control-Allow-Origin" not in response.headers
    response = client.options(
        "/missing",
        headers={"Origin": "https://client.example", "Access-Control-Request-Method": "DELETE"},
    )
    assert "Access-Control-Allow-Methods" not in response.headers
