"""Handles all API requests and response processing."""
import requests
import json
import os


sieel_slug = "ignamt-sieel"
sieel_id = 6

# login = requests.post(AUTH_URL,
#                       headers=headers,
#                       data=json.dumps(data))

# auth_token = login.json()["auth_token"]
auth_token = "eyJ1c2VyX2F1dGhlbnRpY2F0aW9uX2lkIjo1MH0:1hW9TL:"\
             "2gZEaaGultNC0S8n-RCmFs6VUHc"

# headers.update({"Authorization": "Bearer "+auth_token})

# userstories = requests.get(API_URL+"userstories?project={}".format(sieel_id),
                        #    headers=headers)


class TaigaAPI:
    """API class to connect to and interact with the Taiga API."""

    def __init__(self, project_slug):
        """Init TaigaAPI with default attr to specific project."""
        self.slug = project_slug
        self.project_id = ""
        self.config_filename = os.path.join("taiga_report", "api.cfg")
        self.host = "https://taiga.leafnoise.io/api/v1/"
        self.auth_url = self.host + "auth"
        self.headers = {"content-type": "application/json",
                        "x-disable-pagination": "True"}
        self.login_data = {"type": "normal",
                           "username": "ignamt",
                           "password": "tanoira1"}
        self.authenticated = False

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

    def _save_auth(self, auth_token, cfg_json, cfg_file):
        cfg_json["auth_token"] = str(auth_token)
        json.dump(cfg_json, cfg_file)

    def _auth(self):
        """Add auth_token to request headers or get new one if none stored."""
        with open(self.config_filename, "r+") as file:
            cfg_json = json.load(file)
            file.seek(0)
            if "auth_token" in cfg_json:
                print("Using past stored authentication token.")
                self._add_auth_token(cfg_json["auth_token"])
                self.authenticated = True
            else:
                auth_token = self._login()
                self._add_auth_token(auth_token)
                self._save_auth(auth_token=auth_token,
                                cfg_json=cfg_json,
                                cfg_file=file)
                self.authenticated = True

    def _add_auth_token(self, auth_token):
        self.headers["Authorization"] = "Bearer " + auth_token

    def _project_id(self):
        if not self.project_id:
            url = self.host + "projects/by_slug?slug=" + self.slug
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self.project_id = response.json().get("id")



    def get_user_stories(self):
        """Get the user stories from the project at the specified slug.
        
        RETURNS: List of dicts with all the info about the user stories in the 
        'DONE' category
        """
        if not self.authenticated:
            self._auth()
        self._project_id()
        done_id = self._get_done_status()
        us_uri = "userstories?project={}&status={}".format(self.project_id,
                                                           done_id)
        project_us_url = self.host + us_uri
        user_stories = requests.get(project_us_url,
                                    headers=self.headers)
        user_stories.raise_for_status()

        return user_stories.json()
        


class APIError(Exception):
    """Exception raised for any errors caused by API.

    If the API is no not responding or is not working as intended.
    Works like a regular Exception.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
