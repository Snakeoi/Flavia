import json
from .fixtures.app_fixtures import app


def test_map_view():
    with app.test_request_context():
        with app.test_client() as client:
            response = client.get("/map")

            assert response.status_code == 200
            assert isinstance(json.loads(response.text), list)
