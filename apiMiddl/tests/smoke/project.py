from utils import * 
import json
from sys import exit

def create_project(data):

    print("Tworzę sesję... ", end ="")

    d  = {
            "name": random_str(10),
            "about": "this is a test project for testing purposes"
    }

    r = data['session'].post(url("accounts/projects"), json=d)
    assert_ret_code(r, 201)
    d = json.loads(r.content)
    print("Created project with id: %d" % int(d['id']))

    data['project_id'] = int(d['id'])

    return data

def get_project(data):
    r = data['session'].get(url("accounts/projects"))
    projects = json.loads(r.content)

    for project in projects:
        if project['id'] == data['project_id']:
            print("We got out projects!")
            print(project)
            break
        exit("Missing project with out id")

    return data
