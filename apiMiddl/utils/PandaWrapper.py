import pandas as pd
from pandas_profiling import ProfileReport
import threading
import time

def generate_science_data_html(file_handle, profile=None):

    df = pd.read_csv(file_handle)
    records, columns = df.shape
    profile = ProfileReport(df, minimal=True)
    #j = profile.to_notebook_iframe()

    path = "/tmp/a.html"
    profile.to_file( path )
    html = open(path, 'r').read()
    return html

def generate_science_data_json(file_handle, profile=None):

    df = pd.read_csv(file_handle)
    records, columns = df.shape
    profile = ProfileReport(df, minimal=True)
    j = profile.to_json()
    return j

def s(file_handle):
    profile = None

    t = threading.Thread(target=generate_science_data,
            args = (file_handle, profile))
    t.start()

    print("Waitign for join")
    t.join()
    #print(profile)

if __name__ == "__main__":
    print(s(open("/home/ohai/train.csv")))
