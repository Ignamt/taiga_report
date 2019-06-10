"""Test for the TaigaAPI."""
import pytest
import io
import json
import os
import tempfile
import requests

from taiga_report import taiga_api

@pytest.fixture
def api():
    return taiga_api.TaigaAPI("ignamt-sieel")

def test_api_creation(api):
    """Test the example api is instantiated correctly."""
    assert api.slug == "ignamt-sieel"
    assert api.auth_url == "https://taiga.leafnoise.io/api/v1/auth"
    assert api.host == "https://taiga.leafnoise.io/api/v1/"
    assert api.headers == {"content-type": "application/json",
                           "x-disable-pagination": "True"}


def test_api_login(api):
    """Test that login method returns string content."""
    login_data = api._login()
    assert login_data
    assert isinstance(login_data, str)


def test_api_login_request_failure(api):
    """Test if exception is raised when login fails."""
    with pytest.raises(requests.exceptions.HTTPError):
        api.auth_url = api.auth_url.replace("auth", "hola")
        api._login()


def test_api_save_auth(api):
    """Test if auth_token is saved on a file."""
    auth_token = "testauthtoken"
    cfg_file = io.StringIO('{"auth_token": ""}')
    cfg_json = json.load(cfg_file)
    api._save_auth(auth_token, cfg_json, cfg_file)

    assert cfg_json["auth_token"] == "testauthtoken"


def test_api_auth_with_saved_token(api):
    """Test if _auth registers auth_token in file object (via mock-file)."""
    filename = os.path.join(tempfile.gettempdir(), "test_api.cfg")
    with open(filename, "w") as file:
        file.write('{"auth_token": "testauthtoken"}')

    api.config_filename = filename
    api._auth()
    assert api.headers["Authorization"] == "Bearer testauthtoken"
    assert api.authenticated


def test_api_auth_without_saved_token(api):
    """Test if _auth saves and registers token."""
    filename = os.path.join(tempfile.gettempdir(), "test_empty_api.cfg")
    empty_file = open(filename, "w+")
    empty_file.write("{}")
    empty_file.seek(0)
    assert empty_file.read() == "{}"
    empty_file.close()

    api.config_filename = filename
    print(api.config_filename)
    print(api.host)
    print(api.headers)
    print(api.login_data)
    api._auth()
    assert api.authenticated
    with open(filename, "r") as saved_file:
        assert '"auth_token": "' in saved_file.read()


def test_add_auth_token(api):
    """Test that token is added to headers."""
    api._add_auth_token("holaquetal")
    assert "Authorization" in api.headers
    assert api.headers["Authorization"] == "Bearer holaquetal"


def test_api_get_user_stories(api):
    pass
