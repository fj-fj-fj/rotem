from app import app
from tests.conftest import captured_templates


client = app.test_client()


def test_page_not_found():
    with captured_templates(app) as templates:
        r = client.get("/foo")
        assert r.status_code == 404
        template, _ = templates[0]
        assert template.name == "errors/404.html"
        assert b"<h1>404</h1>" in r.data


def test_internal_server_error():
    with captured_templates(app) as templates:
        r = client.get("/__500")
        assert r.status_code == 500
        template, _ = templates[0]
        assert template.name == "errors/500.html"
        assert b"<h1>500</h1>" in r.data
