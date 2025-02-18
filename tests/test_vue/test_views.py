import re

import pytest

from ..fixtures.app_fixtures import app


def test_main_view():
    with app.test_request_context():
        with app.test_client() as client:
            response = client.get("/")
            data_str = str(response.data)

            assert response.status_code == 200
            assert re.search(r'<div id="app">', data_str)
            assert re.search(r"static/assets/index-.*\.js", data_str)
            assert re.search(r"static/assets/index-.*\.css", data_str)


def test_other_view():
    with app.test_request_context():
        with app.test_client() as client:
            response = client.get("/other")
            data_str = str(response.data)

            assert response.status_code == 200  # Will always be 200 in tests because it depends on vue-router.
            assert re.search(r'<div id="app">', data_str)
            assert re.search(r"static/assets/index-.*\.js", data_str)
            assert re.search(r"static/assets/index-.*\.css", data_str)


@pytest.mark.skip(reason="Not implemented yet.")
def test_api_route():
    pass


def test_static_files_route_for_existing_file():
    with app.test_request_context():
        with app.test_client() as client:
            response = client.get("/static/favicon.ico")

            assert response.status_code == 200


def test_static_files_route_for_non_existing_file():
    with app.test_request_context():
        with app.test_client() as client:
            response = client.get("/static/rick_roll.mp4")

            assert response.status_code == 404
