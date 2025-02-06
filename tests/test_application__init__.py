from .fixtures.app_fixtures import app_db_create_destroy

def test_if_config_is_test_config(app_db_create_destroy):
    with app_db_create_destroy.app_context():
        assert app_db_create_destroy.config['TESTING'] == True