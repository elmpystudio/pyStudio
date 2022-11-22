from utils import * 

def db_private(session):

    r = session['session'].get(url("items/dashboard/private"))
    assert_ret_code(r, 200)
    print(r.content)

    return session


def db_purchased(session):

    r = session['session'].get(url("items/dashboard/purchased"))
    assert_ret_code(r, 200)
    print(r.content)

    return session
