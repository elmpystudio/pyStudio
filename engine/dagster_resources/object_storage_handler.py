from minio import Minio
from dagster_resources import engine_config as conf
import pickle as pkl
import io
import ast
import pandas as pd
import dill
import pandas as pd
from s3fs import S3FileSystem
import pyarrow.parquet as pq

minioClient = Minio(conf.OBJECT_STORAGE_HANDLER['connection_string'],
                    access_key=conf.OBJECT_STORAGE_HANDLER['access_key'],
                    secret_key=conf.OBJECT_STORAGE_HANDLER['secret_key'],
                    secure=False)


def initialize_minio_server():
    if not minioClient.bucket_exists('datasets'):
        minioClient.make_bucket('datasets')

    if not minioClient.bucket_exists('deployed-objects'):
        minioClient.make_bucket('deployed-objects')


def get_deployed_wf_model(model_name):
    return pkl.load(minioClient.get_object('deployed-objects', model_name))


def put_deployed_wf_model(model_object, model_name):
    model_bytes = pkl.dumps(model_object)
    return minioClient.put_object('deployed-objects', model_name, io.BytesIO(model_bytes), len(model_bytes))


def get_deployed_wf_interpreter(model_name):
    return dill.load(minioClient.get_object('deployed-objects', model_name))


def put_deployed_wf_interpreter(model_object, model_name):
    model_bytes = dill.dumps(model_object)
    minioClient.put_object('deployed-objects', model_name, io.BytesIO(model_bytes), len(model_bytes))


def put_deployed_wf_object_from_file(original_file_path, object_name):
    minioClient.fput_object('deployed-objects', object_name, original_file_path)


def get_deployed_wf_object(object_name):
    return minioClient.get_object('deployed-objects', object_name).read()


def get_prebuilt_model(model_name):
    return minioClient.get_object('pre-built', model_name + '.model'), minioClient.get_object('pre-built',
                                                                                              model_name + '.lime')


def read_dataset_metadata(dataset_name):
    return ast.literal_eval(
        minioClient.get_object('datasets', dataset_name.replace('.csv', '.json')).read().decode("utf-8"))


def read_dataset(dataset_name, data_types=None, delimiter=','):
    return pd.read_csv(io.BytesIO(minioClient.get_object('datasets', dataset_name).read()),
                       encoding='utf8', dtype=data_types, header=0)


def read_dataset_sample(dataset_name, data_types=None, delimiter=','):
    import random
    return pd.read_csv(io.BytesIO(minioClient.get_object('datasets', dataset_name).read()),
                       encoding='utf8', dtype=data_types, header=0, skiprows=lambda i: i > 0 and random.random() > 0.1)


def read_dataframe(run_id, node_name, output_seq):
    s3 = S3FileSystem(client_kwargs={'endpoint_url': "http://" + conf.OBJECT_STORAGE_HANDLER['connection_string']})
    dataset = pq.ParquetDataset(
        "s3://dagster-test/dagster/storage/{run_id}/intermediates/{node_name}.compute/{output_seq}".format(
            run_id=run_id,
            node_name=node_name, output_seq=output_seq), filesystem=s3)
    df = dataset.read_pandas().to_pandas()
    return df
