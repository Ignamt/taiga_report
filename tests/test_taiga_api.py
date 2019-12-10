"""Test for the TaigaAPI."""
import pytest
import requests

from taiga_report.api import taiga_api


@pytest.fixture
def api():
    """Return a new api object for each function as needed."""
    yaml_dict = {
        'headers': {
            'content-type': 'application/json',
            'x-disable-pagination': 'True'
        },
        'sieel': {
            'slug': 'ignamt-sieel',
            'id': 6,
            'done_id': 35,
            'report_sections': [
                'general',
                'expedientes',
                'remitos',
                'administracion'
            ],
            'host': 'https://taiga.leafnoise.io/api/v1/',
            'login_data': {
                'type': 'normal',
                'username': 'ignamt',
                'password': 'tanoira1'
            }
        }
    }

    return taiga_api.TaigaAPI("sieel", yaml_dict)


def test_api_creation(api):
    """Test the example api is instantiated correctly."""
    assert api.slug == "ignamt-sieel"
    assert api.auth_url == "https://taiga.leafnoise.io/api/v1/auth"
    assert api.host == "https://taiga.leafnoise.io/api/v1/"


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


def test_api_auth_with_saved_token(api):
    """Test if _auth uses same token if already provided."""
    api.auth_token = "testauthtoken"
    api._auth()
    assert api.headers["Authorization"] == "Bearer testauthtoken"
    assert api.authenticated


def test_api_auth_without_saved_token(api):
    """Test if _auth saves and registers token."""
    api.auth_token = None
    assert not api.auth_token

    api._auth()
    assert api.authenticated
    assert api.auth_token


def test_add_auth_token(api):
    """Test that token is added to headers."""
    api._add_auth_token("holaquetal")
    assert "Authorization" in api.headers
    assert api.headers["Authorization"] == "Bearer holaquetal"


def test_api_download_user_stories(api):
    """Test that api gets list of user stories."""
    userstories = api.download_user_stories()
    print("User stories: " + str(userstories))
    assert isinstance(userstories, list)
    assert len(userstories)


def test_api_download_us_failure_raises_exception(api):
    """Test that download us method raises exception upon error."""
    with pytest.raises(requests.exceptions.HTTPError):
        api.host = api.host + "hola/"
        api.download_user_stories()


def test_api_get_done_status_id(api):
    """Test that api gets the done status id."""
    api._auth()
    done_id = api._get_done_status()
    assert done_id == 35


def test_api_get_done_status_not_found(api):
    """Test that HTTPError is raised when request fails."""
    with pytest.raises(requests.exceptions.HTTPError):
        api.host = api.host+"/hola/"
        api._get_done_status()


def test_api_getting_project_id(api):
    """Test that api can get project id."""
    assert api.project_id == 6
