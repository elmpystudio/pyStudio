from utils import * 

def mp_set_offering(session):

    print("Creating new offering")

    d  = {
            "title": random_str(10),
            "tags": [
                {"name": "tag1"},
                {"name": "tag2"},
                {"name": "tag3"},
                {"name": "tag4"},
                    ],
            "price": 42069,
            "item": session['dataset_id'],
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


def mp_get_offering(session):

    r = session['session'].get(url("marketplace/offering"))
    assert_ret_code(r, 200)
    result = r.json()
    print(r.content)

    #print("Getting all offers: %s" % result['key'])
    return session

def mp_purchase(session):

    d = {
            "offering": session['offering_id'],
            "price": 10,
            "period": 10
    }

    r = session['session'].post(url("marketplace/purchase"), json=d)
    assert_ret_code(r, 200)
    print(r.content)

    return session
