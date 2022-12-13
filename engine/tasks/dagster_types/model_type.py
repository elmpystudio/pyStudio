import os

from dagster import (
    PythonObjectDagsterType,
)

from dagster.core.storage.system_storage import fs_system_storage
from dagster.core.storage.type_storage import TypeStoragePlugin
from pyspark.ml import PipelineModel
import joblib
from s3fs import S3FileSystem

from tasks.dagster_types.tasks_metadata import TaskModelOutputMetaData, TaskMetaData
from tasks.ml_menu_generator import get_task_params
import json
from dagster_resources import engine_config as conf


class SparkDataFrameS3StoragePlugin(TypeStoragePlugin):  # pylint: disable=no-init
    @classmethod
    def compatible_with_storage_def(cls, system_storage_def):
        try:
            from dagster_aws.s3.system_storage import s3_system_storage

            return system_storage_def is s3_system_storage
        except ImportError:
            return False

    
    @classmethod
    def set_object(cls, intermediate_store, obj, _context, _runtime_type, paths):
        target_path = intermediate_store.object_store.key_for_paths(paths)
        if not _context.mode_def.name=='heavy':
            s3 = S3FileSystem(client_kwargs={'endpoint_url': "http://" + conf.OBJECT_STORAGE_HANDLER['connection_string']})
            with s3.open(intermediate_store.uri_for_paths(paths, protocol='s3://')+".pkl",'wb') as data_file:
                joblib.dump(obj[0], data_file)
            with s3.open(intermediate_store.uri_for_paths(paths, protocol='s3://')+'_pipeline.pkl', 'wb') as data_file:
                joblib.dump(obj[1], data_file)
            # if _context.solid_def.name!='FitModel':
            model_md={}
            keys = get_task_params(_context.solid_def.name).keys()
            for k in keys:
                if _context.solid_def.name == 'FitModel':
                    model_md[k] = getattr(obj[0], 'target')
                else:
                    try:
                        model_md[k] = getattr(obj[0].model, k)
                    except Exception as e:
                        # some people does not follow standar way of sklearn like catBoost obj will work here
                        model_md[k] = obj[0].model._init_params.get(k)

            meta_data=TaskModelOutputMetaData(1, "BottomCenter" if paths[2]=="BottomLeft" else paths[2], model_md=model_md)
            meta=TaskMetaData(_context.solid_def.name, paths[1].split('.')[0])
            meta.add_output_meta_data(meta_data)
            with open('/tmp/dagster/{id}/{id}_{step}_output_model_1.model_meta_data.json'.format(id=_context.run_id, step=paths[1].split('.')[0]),'w') as meta_file:
                json.dump(meta.to_dict(), meta_file)
        else:
            obj[0].write().overwrite().save(intermediate_store.uri_for_paths(paths, protocol='s3a://'))
        return target_path

    @classmethod
    def get_object(cls, intermediate_store, context, _runtime_type, paths):
        if not context.mode_def.name=='heavy':
            s3 = S3FileSystem(client_kwargs={'endpoint_url': "http://" + conf.OBJECT_STORAGE_HANDLER['connection_string']})
            with s3.open(intermediate_store.uri_for_paths(paths, protocol='s3://')+".pkl") as data_file:
                model=joblib.load(data_file)
            pipe=joblib.load(s3.open(intermediate_store.uri_for_paths(paths, protocol='s3://')+'_pipeline.pkl', 'rb'))
            return [model, pipe]
        else:
            return [PipelineModel.load(
                intermediate_store.uri_for_paths(paths, protocol='s3a://')
            ), []]

    @classmethod
    def required_resource_keys(cls):
        return frozenset({'pyspark'})


class SparkDataFrameFilesystemStoragePlugin(TypeStoragePlugin):  # pylint: disable=no-init
    @classmethod
    def compatible_with_storage_def(cls, system_storage_def):
        return system_storage_def is fs_system_storage

    @classmethod
    def set_object(cls, intermediate_store, obj, _context, _runtime_type, paths):
        target_path = os.path.join(intermediate_store.root, *paths)
        obj[0].write().overwrite().save(intermediate_store.uri_for_paths(paths))
        return target_path

    @classmethod
    def get_object(cls, intermediate_store, context, _runtime_type, paths):
        return [PipelineModel.load(
            os.path.join(intermediate_store.root, *paths)
        ), []]

    @classmethod
    def required_resource_keys(cls):
        return frozenset({'pyspark'})


PipelineType = PythonObjectDagsterType(
    python_type=list,
    name='PySparkPipelineModel',
    description='A Pyspark pipeline model.',
    auto_plugins=[SparkDataFrameS3StoragePlugin, SparkDataFrameFilesystemStoragePlugin],
    # output_materialization_config=spark_df_output_schema,
)