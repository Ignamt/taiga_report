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
    host = "https://taiga.leafnoise.io/api/v1/"
    auth_url = host + "auth"
    headers = {"content-type": "application/json",
               "x-disable-pagination": "True"}
    config_file = os.sep.join(["taiga_report", "api.cfg"])

    def __init__(self, project_slug):
        """Init TaigaAPI with default attr to specific project."""
         
        self.login_data = {"type": "normal",
                           "username": "ignamt",
                           "password": "tanoira1"}
        self.slug = project_slug

        # self._auth()

    def _login(self):
        login_data = requests.post(self.auth_url,
                                   headers=self.headers,
                                   data=json.dumps(self.login_data))
        return login_data.json()

    def _save_auth(self, auth_token, cfg_json, cfg_file):
        cfg_json["auth_token"] = str(auth_token)
        json.dump(cfg_json, cfg_file)
        cfg_file.save()

    def _auth(self):
        pass
