from utils import *
import requests

def file_upload(data):

    file_name = "train.csv"
    u = url("items/file_upload/" + file_name)
    #files = {'upload_file': "test123test"}
    files = {file_name: open('tests/smoke/' + file_name).read()}

    r = data['session'].post(u, files=files)
    assert_ret_code(r, 200)
    print("File uploaded:" + r.content.decode())

    data['file_id'] = r.json()['id']

    return data

if __name__ == "__main__":
    file_upload()

