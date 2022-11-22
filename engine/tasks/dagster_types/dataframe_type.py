import os
from dagster import (
    Bool,
    Field,
    Materialization,
    Path,
    PythonObjectDagsterType,
    String,
    check,
    resource,
)
from dagster.config.field_utils import Selector
from dagster.core.storage.system_storage import fs_system_storage
from dagster.core.storage.type_storage import TypeStoragePlugin
from dagster.core.types.config_schema import output_selector_schema
from s3fs import S3FileSystem
from .tasks_metadata import TaskDataOutputMetaData, TaskMetaData
import json
from dagster_resources import engine_config as conf

s3 = S3FileSystem(client_kwargs={'endpoint_url': "http://" + conf.OBJECT_STORAGE_HANDLER['connection_string']})

# this is a dictionary used as cache for the temporal inputs and outputs,
# it is part of the technical dept that we have, (maybe model_type will be to be fixed too)
# as ideally for doing this the best is to avoid using files,
# as you see some files are just being created but not used,
# using this cache give us 10secs less in execution time
test_fast = {}


def save_funny_files(meta_data, name, id,  paths, obj, uri):
    meta = TaskMetaData(name, paths[1].split('.')[0])
    meta.add_output_meta_data(meta_data)
    file_path = '/tmp/dagster/{id}/{id}_{step}_task_meta_data.json'.format(id=id,
                                                                        step=paths[1].split('.')[0])
    # here to add obj output to have more info at frontEnd!
    meta_data_dic = meta_data.to_dict()
    meta_dic = meta.to_dict()
    if name == 'CategoryEncoding':
        meta_data_dic['dtypes'].update({'mappings': obj[1][1].mapping})
        meta_dic['outputs'][0]['dtypes'].update({'mappings': obj[1][1].mapping})

    if os.path.isfile(file_path):
        meta_data.output_sequence = 2
        with open(file_path, 'r+') as meta_file:
            dat = json.load(meta_file)
            meta_file.seek(0)
            dat['outputs'].append(meta_data_dic)

            json.dump(dat, meta_file)
            meta_file.truncate()
    else:
        with open(file_path, 'w+') as meta_file:
            meta_file.write(json.dumps(meta_dic, default=str))


@output_selector_schema(
    Selector(
        {
            'csv': {
                'path': Field(Path),
                'sep': Field(String, is_required=False),
                'header': Field(Bool, is_required=False),
            },
        }
    )
)
def spark_df_output_schema(_context, file_type, file_options, spark_df):
    if file_type == 'csv':
        spark_df.write.csv(
            file_options['path'], header=file_options.get('header'), sep=file_options.get('sep')
        )
        return Materialization.file(file_options['path'])
    else:
        check.failed('Unsupported file type: {}'.format(file_type))


# here some technical dept
def middle_pkl(obj, uri):
    s3.open(uri + '.pkl', 'wb')


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
        global test_fast
        target_path = intermediate_store.object_store.key_for_paths(paths)
        if not _context.mode_def.name == 'heavy':

            uri = intermediate_store.uri_for_paths(paths, protocol='s3://')
            my_id = uri[uri.index("flowchartNode"):]
            test_fast[paths[2]] = obj
            test_fast[my_id] = obj[1]

            middle_pkl(obj, uri)

            meta_data = TaskDataOutputMetaData(sample_df=obj[0].sample(5), o_sequence=1,
                                               o_label=paths[2], dtypes=obj[0].dtypes.map(
                    lambda x: 'category' if x == 'object' else str(x)).to_dict(),
                                               number_of_records=obj[0].shape[0], df_description=obj[0].describe(),
                                               df_info='')

            save_funny_files(meta_data, _context.solid_def.name, _context.run_id, paths, obj, uri)
        else:
            obj[0].write.parquet(intermediate_store.uri_for_paths(paths, protocol='s3a://'))

        return target_path

    @classmethod
    def get_object(cls, intermediate_store, context, _runtime_type, paths):
        global test_fast
        if not context.mode_def.name == 'heavy':
            uri = intermediate_store.uri_for_paths(paths, protocol='s3://')
            my_id = uri[uri.index("flowchartNode"):]
            try:
                table = test_fast.get(paths[2])
            except Exception:
                print("exception on getting dataset")

            try:
                pipe = test_fast.get(my_id)
            except Exception:
                print("exception on getting THE PIPE, a pkl...")

            return [table[0], pipe]
        else:
            return [context.resources.pyspark.spark_session.builder.getOrCreate().read.parquet(
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
        print("kaka Set_object")
        target_path = os.path.join(intermediate_store.root, *paths)
        obj[0].write.parquet(intermediate_store.uri_for_paths(paths))
        return target_path

    @classmethod
    def get_object(cls, intermediate_store, context, _runtime_type, paths):
        print("kaka Get_object")
        return [context.resources.pyspark.spark_session.builder.getOrCreate().read.parquet(
            os.path.join(intermediate_store.root, *paths)
        ), []]

    @classmethod
    def required_resource_keys(cls):
        print("required_resource_keys")
        return frozenset({'pyspark'})


DataFrame = PythonObjectDagsterType(
    python_type=list,
    name='PySparkDataFrame',
    description='A Pyspark data frame.',
    auto_plugins=[SparkDataFrameS3StoragePlugin, SparkDataFrameFilesystemStoragePlugin],
    output_materialization_config=spark_df_output_schema,
)
