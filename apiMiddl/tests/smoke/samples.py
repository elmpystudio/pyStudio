
from utils import * 

def ds_get_sample(session):

    r = session['session'].get(url("items/sample/%d") % session['dataset_id'])
    assert_ret_code(r, 200)
    print(r.content)

    return session

def ds_get_raport(session):

    r = session['session'].get(url("items/raport/json/%d") % session['dataset_id'])
    assert_ret_code(r, 200)

    r = session['session'].get(url("items/raport/html/%d") % session['dataset_id'])
    assert_ret_code(r, 200)
    #print(r.content)

    return session
