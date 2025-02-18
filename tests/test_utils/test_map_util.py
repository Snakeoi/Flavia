import json

from tests.fixtures.app_fixtures import app

from application.utils import map

def test_map():
    with app.app_context():
        response = map.view()

        assert response.status_code == 200
        assert isinstance(json.loads(response.data), list)
        assert len(json.loads(response.data)) > 1
        assert json.loads(response.data)[0].keys() == {"endpoint", "url", "method"}


