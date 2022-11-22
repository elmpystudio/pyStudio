import requests
import json
from utils import * 


def register(r):

    data = {
                "username": random_str(10),
                "email": random_str(10)+"@gmail.com",
                "password": "q1",
                "session": r
            }

    print("Registering with data: " + str(data))

    r = data['session'].post(url("register"), json={
            "email": data['email'],
            "password": data['password'],
            "username": data['username'],
        })
    
    assert_ret_code(r, 200)
    for key,value in r.headers.items():
        print("%s: %s" % (key,value))

    result = json.loads(r.content)['result']

    if result == True:
        print("Register OK!")
    else:
        print("Register Fail!")
        print("Status code: %d" % r.status_code)
        print("Content: " + r.content.decode())

    return data

def login(data):

    print("Loggin with data: %s %s" % (data['email'], data['password']))

    r = data['session'].post(url("token"), json= {
            "email": data['email'],
            "password": data['password'],
        })

    assert_ret_code(r, 200)
    print("Login OK!")
    token = r.json()['access']

    headers ={
        "Authorization": "bearer " + token,
    }

    data['session'].headers.update(headers)
    return data


def about(data):

    r = data['session'].get(url("accounts/users"))
    assert_ret_code(r, 200)

    d = json.loads(r.content)
    print("Nasze id: %d" % (d['id']))

    try:
        json.loads(r.content)
        print("About OK!")
    except:
        print("About FAIL!")

