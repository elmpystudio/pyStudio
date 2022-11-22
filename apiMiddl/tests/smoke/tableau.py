from utils import * 
import requests

def tab(data):

    d = {
            'ip': requests.get("https://icanhazip.com/").content.decode().strip()
    }
    r = data['session'].post(url("tableau/trusted"), data=d)

    assert_ret_code(r, 200)
    result = r.json()
    print("Get tab key: %s" % result['key'])

    return data
