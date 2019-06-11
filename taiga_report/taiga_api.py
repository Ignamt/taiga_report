"""Handles all API requests and response processing."""
import requests
import json
import os


class TaigaAPI:
    """API class to connect to and interact with the Taiga API."""

    def __init__(self, project_slug):
        """Init TaigaAPI with default attr to specific project."""
        self.slug = project_slug
        self.authenticated = False
        self.auth_token = None
        self.config_filename = os.path.join("taiga_report", "api.cfg")
        self.host = "https://taiga.leafnoise.io/api/v1/"
        self.auth_url = self.host + "auth"
        self.headers = {"content-type": "application/json",
                        "x-disable-pagination": "True"}
        self.login_data = {"type": "normal",
                           "username": "ignamt",
                           "password": "tanoira1"}
        self.project_id = self._project_id

    def _login(self):
        """Log the api object to Taiga's API.

        RETURNS: a str() of the auth_token

        RAISES:
            - requests.exceptions.HTTPError if the request fails. (via
                raise_for_status()

        """
        response = requests.post(self.auth_url,
                                 headers=self.headers,
                                 data=json.dumps(self.login_data))

        # Raises http exception if status_code not ok.
        response.raise_for_status()

        return response.json()["auth_token"]

    def _auth(self):
        """Add auth_token to request headers or get new one if none stored."""
        if not self.auth_token:
            print("No auth_token detected, logging in.")
            self.auth_token = self._login()
        self._add_auth_token(self.auth_token)
        self.authenticated = True

    def _add_auth_token(self, auth_token):
        self.headers["Authorization"] = "Bearer " + auth_token

    @property
    def _project_id(self):
        if not self.authenticated:
            self._auth()
        url = self.host + "projects/by_slug?slug=" + self.slug
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("id")

    def download_user_stories(self):
        """Get the user stories from the project at the specified slug.
        
        RETURNS: List of dicts with all the info about the user stories in the
        'DONE' category
        """
        if not self.authenticated:
            self._auth()
        # done_id = self._get_done_status()
        us_uri = "userstories?project={}".format(self.project_id)
        project_us_url = self.host + us_uri
        user_stories = requests.get(project_us_url,
                                    headers=self.headers)
        user_stories.raise_for_status()

        return user_stories.json()

    def _get_done_status(self):
        """Get the status id from the API to filter user stories."""
        url = self.host + "userstory-statuses"
        us_statuses = requests.get(url, headers=self.headers)
        us_statuses.raise_for_status()

        for us_status in us_statuses.json():
            if us_status.get("slug") == "done":
                print("US Status: ", us_status)
                return us_status["id"]


class APIError(Exception):
    """Exception raised for any errors caused by API.

    If the API is no not responding or is not working as intended.
    Works like a regular Exception.
    """

    def __init__(self, *args, **kwargs):
        """Init the object with regular exception __init__."""
        super().__init__(*args, **kwargs)
