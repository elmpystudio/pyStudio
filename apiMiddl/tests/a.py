import requests

def get_url(endpoint):
    host = "http://tab.entomu.com:8999/%s"
    return host % endpoint

signin_url = get_url("/api/3.6/auth/signin")

payload = """
<tsRequest>
  <credentials name="{username}" password="{password}" >
    <site contentUrl="{content_url}" />
  </credentials>
</tsRequest>
""".format(username="api-user", password="Aa123456", content_url="API").strip()

payload = """
{
    "credentials": {
      "name": "%s",
      "password": "%s",
      "site": {
        "contentUrl": "%s"
      }
    }
  }
""" % ("api-user", "Aa123456", "API")

print(payload)

import json
headers = {"Accept": "application/json", "Content-Type": "application/json"}
r = requests.post(signin_url, json= json.loads(payload), headers=headers)
print(r.status_code)
print(r.content)
