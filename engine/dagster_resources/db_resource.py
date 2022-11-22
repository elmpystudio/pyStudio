import psycopg2
from minio import Minio
from minio.error import ResponseError
import os
import shutil
from dagster_resources import engine_config as conf


def deleteFolder(bucketname, folderName):

    minioClient = Minio(conf.OBJECT_STORAGE_HANDLER['connection_string'],
                    access_key=conf.OBJECT_STORAGE_HANDLER['access_key'],
                    secret_key=conf.OBJECT_STORAGE_HANDLER['secret_key'],
                    secure=False)
    # Delete using "remove_object"
    objects_to_delete = minioClient.list_objects(bucketname, prefix=folderName, recursive=True)
    for obj in objects_to_delete:
        minioClient.remove_object(bucketname, obj.object_name)


def delete_dataset(id):
    try:
        deleteFolder('dagster-test', 'dagster/storage/{id}'.format(id=id))
    except Exception:

        pass


def delete_metadata(id):
    path="/tmp/dagster/{id}".format(id=id)

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
    else:
        print("trying to delete nothing...")

    os.makedirs(path, exist_ok=True)
    connection1, connection2=(False, False)
    try:
        connection1 = psycopg2.connect(
                **conf.DB_HANDLER_CONFIG,
                database="test_event_log_storage")

        cursor1 = connection1.cursor()
        postgreSQL_select_Query = """
        DELETE FROM event_logs
        WHERE run_id='{id}'
        """.format(id=id)

        cursor1.execute(postgreSQL_select_Query)
        connection1.commit()
        
        connection2 = psycopg2.connect(
                **conf.DB_HANDLER_CONFIG,
                database="test_run_storage")

        cursor2 = connection2.cursor()
        postgreSQL_select_Query = """
        DELETE FROM runs
        WHERE run_id='{id}'
        """.format(id=id)

        cursor2.execute(postgreSQL_select_Query)
        connection2.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection1):
            cursor1.close()
            connection1.close()
        if(connection2):
            cursor2.close()
            connection2.close()

def read_status(id):
    connection=False
    run_records=[]
    try:

        connection = psycopg2.connect(
                **conf.DB_HANDLER_CONFIG,
                database="test_event_log_storage")

        cursor = connection.cursor()
        postgreSQL_select_Query = """
        select event, dagster_event_type, timestamp from event_logs 
        where run_id='{id}' AND
        (dagster_event_type LIKE 'STEP_%' OR dagster_event_type LIKE 'PIPELINE_%')
        """.format(id=id)

        cursor.execute(postgreSQL_select_Query)
        run_records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        return {'ERROR:': 'Error in Query'}

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
    if not run_records:
        return False
    else: 
        return run_records
