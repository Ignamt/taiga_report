"""Tests for the TaigaAPI."""
import pytest
import io
import json

from taiga_report import taiga_api


@pytest.fixture
def api():
    """Instance an API to use in tests."""
    return taiga_api.TaigaAPI("ignamt-sieel")


def test_api_creation(api):
    assert api.slug == "ignamt-sieel"
    assert api.auth_url =="https://taiga.leafnoise.io/api/v1/auth"
    assert api.host == "https://taiga.leafnoise.io/api/v1/"
    assert api.headers == {"content-type": "application/json",
                           "x-disable-pagination": "True"}


def test_api_login(api):
    login_data = api._login()
    assert login_data["username"] == "ignamt"


def test_api_save_auth(api):
    auth_token = "testauthtoken"
    cfg_file = MockFile('{"auth_token": ""}')
    cfg_json = json.load(cfg_file)
    api._save_auth(auth_token, cfg_json, cfg_file)

    assert cfg_json["auth_token"] == "testauthtoken"


def test_api_auth(api):
    pass


class MockFile(io.StringIO):
    
    def save(self):
        pass
