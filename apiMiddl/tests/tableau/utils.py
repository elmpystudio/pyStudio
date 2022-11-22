from sys import exit

import string, random

def random_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def url(endpoint):
    return "http://localhost:8000/api/%s/" % endpoint

def assert_ret_code(r, code):
    if r.status_code != code:
        print(r.content)
        exit("Invalid request code, expected: %d, got %d" % (code, r.status_code))

