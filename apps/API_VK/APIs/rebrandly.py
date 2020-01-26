import json

import requests

from secrets.secrets import secrets

api_key = secrets['rebrandly']['api_key']


def get_link(long_url):
    linkRequest = {"destination": long_url,
                   "domain": {
                       "fullName": "rebrand.ly"
                   }
                   # , "slashtag": "A_NEW_SLASHTAG"# ,
                   # "title": "Rebrandly YouTube channel"
                   }

    requestHeaders = {"Content-type": "application/json",
                      "apikey": api_key,
                      # "workspace": "YOUR_WORKSPACE_ID"
                      }

    r = requests.post("https://api.rebrandly.com/v1/links", data=json.dumps(linkRequest), headers=requestHeaders)

    if r.status_code == requests.codes.ok:
        json_result = r.json()["shortUrl"]
        short_link = f'https://{json_result}'
        return short_link
    return None
