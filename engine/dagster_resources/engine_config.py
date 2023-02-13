import os
import pathlib

current_dir = pathlib.Path(__file__).parent.parent
os.environ['DAGSTER_HOME'] = str(current_dir) + '/.dagster_home'

FS_HANDLER_CONFIG = {
    'outputs_path': '/tmp/dagster/',
    'deployment_path': '/tmp/dagster/deployed_models/',
    'datasets_path': '/tmp/dagster/datasets/'
}

DB_HANDLER_CONFIG = {
        'user': "dev" if "AP_PG_USER" not in os.environ else os.environ['AP_PG_USER'],
        "password": "Aa123456" if "AP_PG_PASS" not in os.environ else os.environ['AP_PG_PASS'],
        'host': "localhost" if "AP_PG_HOST" not in os.environ else os.environ['AP_PG_HOST'],
        'port': 5432
}

DB_HANDLER_CONFIG['connection_string']: 'postgresql://{user}:{password}@{host}:{port}/analyticsdb'.format(**DB_HANDLER_CONFIG)

FLASK_CONFIG = {
    'host_ip': '0.0.0.0' if "AP_ML_INTERFACE" not in os.environ else os.environ['AP_ML_INTERFACE'],
    'host_port': 5000 if "AP_ML_PORT" not in os.environ else int(os.environ['AP_ML_PORT']),
}

# minio

OBJECT_STORAGE_HANDLER = {
    'connection_string': "34.91.137.119:9000" if "AP_MINIO_URL" not in os.environ else os.environ['AP_MINIO_URL'],
    'access_key': 'minio' if "AP_MINIO_ACCESS_KEY" not in os.environ else os.environ['AP_MINIO_ACCESS_KEY'],
    'secret_key': 'Aa123456' if "AP_MINIO_SECRET_KEY" not in os.environ else os.environ['AP_MINIO_SECRET_KEY'] ,
    'region_name': "us-east-1",
    'use_unsigned_session': False
}
