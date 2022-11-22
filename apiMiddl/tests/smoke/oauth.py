from register import login
import sys
import requests

r = requests.Session()
r.timeout=30

data = {
            "username": "root",
            "email": "root",
            "password": "w2w2w2W@",
            "session": r
        }

login(data)

url = "http://localhost:8080/hub/login"

r = data['session'].get(url)
print(r.status_code)
print(r.content.decode())
