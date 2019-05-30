"""Handles all API requests and response processing."""
import requests
import pprint

api_url = "https://taiga.leafnoise.io/api/v1/"
auth_url = api_url + "auth"
headers = {"content-type": "application/json"}
data = {"type": "normal", "username": "ignamt", "password": "tanoira1"}
sieel_slug = "ignamt-sieel"
sieel_id = 6

# login = requests.post(auth_url,
#                       headers=headers,
#                       data=json.dumps(data))

# auth_token = login.json()["auth_token"]
auth_token = "eyJ1c2VyX2F1dGhlbnRpY2F0aW9uX2lkIjo1MH0:1hW9TL:"\
             "2gZEaaGultNC0S8n-RCmFs6VUHc"

headers.update({"Authorization": "Bearer "+auth_token,
                "x-disable-pagination": "True"})

userstories = requests.get(api_url+"userstories?project=6",
                           headers=headers)

#TODO: Create

for us in userstories.json():
    #TODO: Check for section tag
        #TODO: 
    
    
    pprint.pprint(us)
    break
