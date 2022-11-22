from utils import *
import requests


def new_va(data):
    print("Creating new va")

    u = url("items/va")
    d = {
            "dataset": data['dataset_id'],
            "name": "smoke_test_" + random_str(10)
    }

    r = data['session'].post(u, data=d, timeout=30)
    assert_ret_code(r, 200)
    resp = r.json()
    print("New va id: %d" % (resp["id"]))
    data['va_id'] = resp["id"]

    return data

def mp_set_va_offering(session):

    print("Creating new VA offering")

    d  = {
            "title": random_str(10),
            "tags": [
                {"name": "tag1"},
                {"name": "tag2"},
                {"name": "tag3"},
                {"name": "tag4"},
                    ],
            "price": 42069,
            "item": session['va_id'],
            "description": "test_description: " + random_str(100),
            "briefDescription": "test_brief_description: " + random_str(100),
            "subscriptionOptionsData": [ {"price": 96, "period": 42}, {"price": 10, "period": 33},  {"price": 1, "period": 3} ]
    }

    r = session['session'].post(url("marketplace/offering"), json=d)
    assert_ret_code(r, 201)
    session['offering_id'] = r.json()['id']
    print(r.content)
    #print("Creating new offering: %s" % r['key'])

    return session



