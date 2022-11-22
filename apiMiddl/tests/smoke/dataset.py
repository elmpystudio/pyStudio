from utils import *
import requests

def new_dataset(data):
    print("Creating new dataset")

    u = url("items/datasets")

    d = {
            "file": data['file_id'],
            "name": "test_dataset",
    }

    r = data['session'].post(u, data=d)
    assert_ret_code(r, 201)
    j = r.content.decode()
    print("New dataset:" + j)
    data['dataset_id'] = r.json()['id']

    return data

if __name__ == "__main__":
    file_upload()

