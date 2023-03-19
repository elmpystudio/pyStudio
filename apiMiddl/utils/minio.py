import ast
import pandas as pd
from minio import Minio
import pickle as pkl
import io
from django.conf import settings
from termcolor import colored as c

MINIO_SERVER_PORT_ = settings.MINIO_SERVER["PORT"]
MINIO_SERVER_IP_ = settings.MINIO_SERVER["IP"]

class MinioWrapper:


    @staticmethod
    def check_if_up():

        import socket
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a_socket.settimeout(3)

        location = (MINIO_SERVER_IP_, MINIO_SERVER_PORT_)
        print(location)
        result_of_check = a_socket.connect_ex(location) 

        if result_of_check != 0: 
            msg = "Minio: couldn't connect to server on %s:%d, check if docker container is up!" % location
            print( c("[-]", 'red') + " " + msg  )

    def __init__(self):

        self.check_if_up()

        print("Initializing minio client start")

        try:
            minio = Minio("%s:%s" % (MINIO_SERVER_IP_, MINIO_SERVER_PORT_),
                                access_key=settings.MINIO_SERVER["ACCESS_KEY"],
                                secret_key=settings.MINIO_SERVER["SECRET_KEY"],
                                secure=False
                    )
            buckets = ["datasets", "assets", "reports"]

            for bucket in buckets:
                if not minio.bucket_exists(bucket):
                    minio.make_bucket(bucket)

            self.minioClient = minio
            print("Initializing minio client done")
        except Exception as e:
            print("Initializing minio client failure")
            print("you will be able to work only using upload CSV in the ML Studio")

    def get(self, bucket, name):
        return self.minioClient.get_object(bucket, name).read()

    def download(self, bucket, name, path):
        return self.minioClient.fget_object(bucket, name, path)

    def getModels(self, user):
        items = []
        for item in Minio.list_objects(self.minioClient, bucket_name="deployed-objects", recursive=True):
            if user in item.object_name:
                items.append(item)
        return items


    ## String bucket / location folder
    ## String name
    ## data CSV??? buffer io object
    ## length
    def put(self, bucket, name, data, length):

        print("[+] Type")
        print(type(data))
        if type(data) == str:
            value_as_bytes = data.encode('utf-8')
            value_as_a_stream = io.BytesIO(value_as_bytes)
            return self.minioClient.put_object(bucket, name, value_as_a_stream, length=len(value_as_bytes))
        else: 
            return self.minioClient.put_object(bucket, name, data, length=length)

minio = 'cofta' #MinioWrapper()
