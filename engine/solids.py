from dagster import solid, Output, OutputDefinition, InputDefinition

from tasks.dagster_types.dataframe_type import DataFrame
from tasks.dagster_types.model_type import PipelineType
import pandas as pd
import xgboost as xgb
import json
from dagster_resources.object_storage_handler import read_dataset, read_dataset_sample, get_deployed_wf_model, \
    read_Kaggle_dataset
import random
from tasks.model_imp.model_lstm import LSTM
from tasks.light import LModeling


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='delimiter', default_value=","
    ), InputDefinition(
        name="dataset_name"
    )],
    required_resource_keys={'pyspark'}
)
def SelectKaggleDataset(context, dataset_name: str, delimiter: str) -> DataFrame:
    tasks = []
    context.log.info(
        'Dataset {named}'.format(named=dataset_name)
    )
    try:
        if not context.mode_def.name == 'heavy':
            df = read_kaggle_dataset(dataset_name, delimiter=delimiter)
            yield Output([df, tasks], 'BottomLeft')
        else:
            df = context.resources.pyspark.spark_session.builder.getOrCreate().read.csv('s3a://' + dataset_name)
            yield Output([df, tasks], 'BottomLeft')
    except Exception as e:
        print(e)


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='delimiter', default_value=","
    ), InputDefinition(
        name="dataset_name"
    )],
    required_resource_keys={'pyspark'}
)
def SelectDataset(context, dataset_name: str, delimiter: str) -> DataFrame:
    tasks = []
    context.log.info(
        'Dataset {named}'.format(named=dataset_name)
    )
    try:
        if not context.mode_def.name == 'heavy':
            df = read_dataset(dataset_name, delimiter=delimiter)
            yield Output([df, tasks], 'BottomLeft')
        else:
            df = context.resources.pyspark.spark_session.builder.getOrCreate().read.csv('s3a://' + dataset_name)
            yield Output([df, tasks], 'BottomLeft')
    except Exception as e:
        print(e)

@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='delimiter', default_value=","
    ), InputDefinition(
        name="dataset_name"
    )],
    required_resource_keys={'pyspark'}
)
def SelectDatasetSample(context, dataset_name: str, delimiter: str) -> DataFrame:
    tasks = []
    context.log.info(
        'Dataset {named}'.format(named=dataset_name)
    )
    if not context.mode_def.name == 'heavy':
        df = read_dataset_sample(dataset_name, delimiter=delimiter)
        yield Output([df, tasks], 'BottomLeft')
    else:
        df = context.resources.pyspark.spark_session.builder.getOrCreate().read.csv('s3a://' + dataset_name)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name="csv_path"
    )],
    required_resource_keys={'pyspark'}
)
def ReadCSV(context, csv_path: str) -> DataFrame:
    tasks = []
    context.log.info(
        'Dataset {named}'.format(named=csv_path)
    )
    print("theeee pathhh" + csv_path)
    if not context.mode_def.name == 'heavy':
        df = pd.read_csv(csv_path)
        yield Output([df, tasks], 'BottomLeft')
    else:
        df = context.resources.pyspark.spark_session.builder.getOrCreate().read.csv('s3a://' + csv_path)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name="csv_path"
    )],
    required_resource_keys={'pyspark'}
)
def ReadCSVSample(context, csv_path: str) -> DataFrame:
    tasks = []
    # csv_path=context.solid_config['csv_path']
    # context.resources.pyspark.spark_session.conf.set("spark.sql.execution.arrow.enabled", "true")
    context.log.info(
        'Dataset {named}'.format(named=csv_path)
    )
    # pipe=PipelineModel(stages=[SelectDatasets(name=name)])
    # df=pipe.transform('')
    if not context.mode_def.name == 'heavy':
        df = pd.read_csv(csv_path,
                         encoding='utf8', dtype=None, header=0,
                         skiprows=lambda i: i > 0 and random.random() > 0.01)
        yield Output([df, tasks], 'BottomLeft')
    else:
        df = context.resources.pyspark.spark_session.builder.getOrCreate().read.csv('s3a://' + dataset_name)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='col_names'
    ), InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    )],
    required_resource_keys={'pyspark'}
)
def SelectColumns(context, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Selected col_name {cols}'.format(cols=col_names)
    )

    if not context.mode_def.name == 'heavy':
        from tasks.light import LSelectColumns
        select_cols = LSelectColumns(col_name=col_names)
        tasks.append(select_cols)
        yield Output([select_cols.transform(df), tasks], 'BottomLeft')
    else:
        pipe = None
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='drop_type'
    ), InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    )],
    required_resource_keys={'pyspark'}
)
def DropMissing(context, drop_type, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Selected drop {cols}'.format(cols=drop_type)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LDropMissing
        # def drop_col_name(df,drop):
        #     return df[drop]
        drop_col_name = LDropMissing(drop=drop_type)
        tasks.append(drop_col_name)
        yield Output([drop_col_name.transform(df), tasks], 'BottomLeft')
    else:

        pipe = None
        df = pipe.transform(df)
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='query'
    ), InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='TopRight', dagster_type=DataFrame, default_value=[None, []]
    )],
    required_resource_keys={'pyspark'}
)
def ApplySqlite(context, query, TopLeft: DataFrame, TopRight) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Selected query {cols}'.format(cols=query)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LApplySqlite
        # def drop_col_name(df,drop):
        #     return df[drop]
        query_task = LApplySqlite(query=query)
        tasks.append(query_task)
        yield Output([query_task.transform(x1=df, x2=TopRight[0]), tasks], 'BottomLeft')
    else:

        pipe = None
        df = pipe.transform(df)

        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='left_col'
    ), InputDefinition(
        name='right_col'
    ), InputDefinition(
        name='join_type'
    ), InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='TopRight', dagster_type=DataFrame, default_value=[None, []]
    )],
    required_resource_keys={'pyspark'}
)
def JoinData(context, left_col, right_col, join_type, TopLeft: DataFrame, TopRight) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Selected left_col {cols}'.format(cols=left_col)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LJoinData
        join_task = LJoinData(left_col=left_col, right_col=right_col, join_type=join_type)

        yield Output([join_task.transform(df1=df, df2=TopRight[0]), tasks], 'BottomLeft')
    else:

        pipe = None
        df = pipe.transform(df)

        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_names'
    )],
    required_resource_keys={'pyspark'}
)
def FillMissingWithMean(context, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    
    context.log.info(
        'Fill missing col_name={cols}'.format(cols=col_names)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LFillMissingWithMean
        lm = LFillMissingWithMean(col_name=col_names)
        data = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([data, tasks], 'BottomLeft')
    else:

        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_names'
    ), InputDefinition(
        name='replacement_value'
    )],
    required_resource_keys={'pyspark'}
)
def FillMissingWithValue(context, col_names, replacement_value, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    
    context.log.info(
        'Fill missing col_name={cols}'.format(cols=col_names)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LFillMissingWithValue
        lm = LFillMissingWithValue(col_name=col_names, value=replacement_value)
        df = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([df, tasks], 'BottomLeft')
    else:

        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_name'
    ), InputDefinition(
        name='no_bins'
    )],
    required_resource_keys={'pyspark'}
)
def ColumnBinning(context, col_name, no_bins, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    
    context.log.info(
        'Fill missing col_name={cols}'.format(cols=col_name)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LColumnBinning
        lm = LColumnBinning(col_name=col_name, no_bins=no_bins)
        df = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([df, tasks], 'BottomLeft')
    else:

        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='changed_columns'
    )],
    required_resource_keys={'pyspark'}
)
def ChangeDtypes(context, changed_columns, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    
    context.log.info(
        'Fill missing col_name={cols}'.format(cols=changed_columns)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LChangeDtypes
        lm = LChangeDtypes(col_name=changed_columns)
        df = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([df, tasks], 'BottomLeft')
    else:

        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='value_to_replace'
    ), InputDefinition(
        name='replacement_value'
    ), InputDefinition(
        name='col_names'
    )],
    required_resource_keys={'pyspark'}
)
def ReplaceValue(context, value_to_replace, replacement_value, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    #     value_to_replace='n'
    context.log.info(
        'Fill missing value_to_replace={cols}'.format(cols=value_to_replace)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LReplaceValue
        lm = LReplaceValue(value_to_replace=value_to_replace, replacement_value=replacement_value, col_names=col_names)
        df = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([df, tasks], 'BottomLeft')
    else:

        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_names'
    )],
    required_resource_keys={'pyspark'}

)
def CategoryEncoding(context, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
 
    context.log.info(
        'Encoded col_name={cols}'.format(cols=col_names)
    )

    if not context.mode_def.name == 'heavy':
        from tasks.light import LCategoryEncoding
        lb = LCategoryEncoding(col_name=col_names)
        df = lb.fit_transform(df)
        tasks.append(lb)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_names'
    )],
    required_resource_keys={'pyspark'}

)
def Normalized(context, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
 
    context.log.info(
        'Encoded col_name={cols}'.format(cols=col_names)
    )

    if not context.mode_def.name == 'heavy':
        from tasks.light import LNormalized
        lb = LNormalized(col_name=col_names)
        df = lb.fit_transform(df)
        tasks.append(lb)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_names'
    )],
    required_resource_keys={'pyspark'}

)
def Standardized(context, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
 
    context.log.info(
        'Encoded col_name={cols}'.format(cols=col_names)
    )

    if not context.mode_def.name == 'heavy':
        from tasks.light import LNormalized
        lb = LNormalized(col_name=col_names)
        df = lb.fit_transform(df)
        tasks.append(lb)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_name_dict'
    )],
    required_resource_keys={'pyspark'}

)
def ChangeColumnsName(context, col_name_dict, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
 
    context.log.info(
        'Encoded col_name={cols}'.format(cols=col_name_dict)
    )

    if not context.mode_def.name == 'heavy':
        from tasks.light import LChangeColumnsName
        lb = LChangeColumnsName(col_name=col_name_dict)
        df = lb.fit_transform(df)

        tasks.append(lb)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='id_vars'
    ), InputDefinition(
        name='value_vars'
    )],
    required_resource_keys={'pyspark'}
)
def MeltingDf(context, id_vars, value_vars, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Encoded id_vars={cols}'.format(cols=id_vars)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LMeltingDf
        lb = LMeltingDf(id_vars=id_vars, value_vars=value_vars)
        df = lb.fit_transform(df)
        tasks.append(lb)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='col_names'
    )],
    required_resource_keys={'pyspark'}

)
def CategoryToDigits(context, col_names, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Encoded col_names={cols}'.format(cols=col_names)
    )

    if not context.mode_def.name == 'heavy':
        from tasks.light import LCategoryToDigits
        lb = LCategoryToDigits(col_names=col_names)
        df = lb.fit_transform(df)
        tasks.append(lb)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='label_column'
    ), InputDefinition(
        name='random_seed'
    ), InputDefinition(
        name='over_sampling_type'
    )],
    required_resource_keys={'pyspark'}
)
def OverSample(context, label_column, random_seed, over_sampling_type, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'Fill missing value_to_replace={cols}'.format(cols=label_column)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LOverSample
        lm = LOverSample(label_column=label_column, random_seed=random_seed, over_sampling_type=over_sampling_type)
        df = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([df, tasks], 'BottomLeft')
    else:
        pipe = None
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='label_column'
    ), InputDefinition(
        name='random_seed'
    ), InputDefinition(
        name='under_sampling_type'
    )],
    required_resource_keys={'pyspark'}
)
def UnderSample(context, label_column, random_seed, under_sampling_type, TopLeft: DataFrame) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    #     value_to_replace='n'
    context.log.info(
        'Fill missing value_to_replace={cols}'.format(cols=label_column)
    )
    if not context.mode_def.name == 'heavy':
        from tasks.light import LUnderSample
        lm = LUnderSample(label_column=label_column, random_seed=random_seed, under_sampling_type=under_sampling_type)
        df = lm.fit_transform(df)
        tasks.append(lm)
        yield Output([df, tasks], 'BottomLeft')
    else:

        pipe = None
        
        tasks.append(pipe)
        yield Output([df, tasks], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', is_required=True, dagster_type=DataFrame
        ),
        OutputDefinition(
            name='BottomRight', is_required=True, dagster_type=DataFrame
        ),
    ],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='partition_percentage', dagster_type=float
    )],
    required_resource_keys={'pyspark'}
)
def SplitData(context, partition_percentage: float, TopLeft: DataFrame):
    tasks = list.copy(TopLeft[1])
    df = TopLeft[0]
    context.log.info(
        'precentage of split={perce}'.format(perce=partition_percentage)
    )
    if not context.mode_def.name == 'heavy':
        cut = (round(partition_percentage * df.shape[0]))
        df = df.sample(frac=1).reset_index(drop=True)
        train = df.iloc[:cut]
        test = df.iloc[cut:]
        yield Output([train, tasks], 'BottomLeft')
        yield Output([test, tasks], 'BottomRight')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='TopRight', dagster_type=DataFrame),
        InputDefinition(
            name='TopLeft', dagster_type=PipelineType),
        InputDefinition(
            name='label_column', dagster_type=str
        )],
    required_resource_keys={'pyspark'}
)
def FitModel(context, label_column: str, TopRight: DataFrame, TopLeft: PipelineType) -> PipelineType:
    tasks = list.copy(TopRight[1])
    df = TopRight[0]
    model = TopLeft[0]

    if not context.mode_def.name == 'heavy':
        model.set_label(target=label_column)
        model.fit(df.drop(label_column, axis=1), df[label_column])

        tasks.append(model)
        # saving pikle in cha ALlah
        model.save()
        yield Output([model, tasks], 'BottomLeft')
    else:
        # pre=HPre_Modeling(inputCol='y_index')
        # model=HModeling(inputCol='y_index', model=model)
        # pipe=Pipeline(stages=[pre, model]).fit(df)
        # tasks.append(pipe)
        # if context.resources.light:
        #     PipelineModel(stages=tasks).write().overwrite().save('/tmp/test')
        yield Output([None, tasks], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='normalize')],
    required_resource_keys={'pyspark'}
)
def LinearRegression(context, normalize) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.linear_model import LinearRegression as LLinearRegression
        
        model = LModeling(context.run_id, LLinearRegression(normalize=normalize), model_name='LinearRegression')
        # model.fit(df)
        # tasks.append(model)
        yield Output([model, []], 'BottomLeft')
    else:
        # pre=HPre_Modeling(inputCol='y_index')
        # model=HModeling(inputCol='y_index', model=model)
        # pipe=Pipeline(stages=[pre, model]).fit(df)
        # tasks.append(pipe)
        # if context.resources.light:
        #     PipelineModel(stages=tasks).write().overwrite().save('/tmp/test')
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='C'),
        InputDefinition(
            name='ratio'),
        InputDefinition(
            name='penalty'),
        InputDefinition(
            name='fit_intercept'),
        InputDefinition(
            name='solver')],
    required_resource_keys={'pyspark'}
)
def LogisticRegressionClassifier(context, C, ratio, penalty, fit_intercept, solver) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.linear_model import LogisticRegression as LLogisticRegression
        

        # solver = 'liblinear'
        if penalty == 'elasticnet':
            solver = 'saga'

        # When l1_ratio must be between 0 and 1
        if solver == 'saga' and ratio == 'none':
            ratio = 0.5

        # liblinear’ does not support setting penalty='none'
        if solver == 'liblinear' and penalty == 'none':
            penalty = 'l2'

        if ratio == 'None':
            ratio = 0.5

        model = LModeling(context.run_id,
                          LLogisticRegression(C=float(C), penalty=penalty, fit_intercept=bool(fit_intercept),
                                              solver=solver,
                                              l1_ratio=ratio), model_name='LogisticRegressionClassifier')

        yield Output([model, []], 'BottomLeft')
    else:
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='criterion'),
        InputDefinition(
            name='max_depth'),
        InputDefinition(
            name='max_leaf_nodes'),
        InputDefinition(
            name='min_samples_leaf'),
        InputDefinition(
            name='min_samples_split'),
        InputDefinition(
            name='random_state')],
    required_resource_keys={'pyspark'}
)
def DecisionTreeClassifier(context, criterion, max_depth, max_leaf_nodes, min_samples_leaf, min_samples_split,
                           random_state) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.tree import DecisionTreeClassifier as LDecisionTreeClassifier
        
        model = LModeling(context.run_id,
                          LDecisionTreeClassifier(criterion=criterion, max_depth=max_depth,
                                                  max_leaf_nodes=max_leaf_nodes,
                                                  min_samples_leaf=min_samples_leaf,
                                                  min_samples_split=min_samples_split,
                                                  random_state=random_state),
                          model_name='DecisionTreeClassifier')
        yield Output([model, []], 'BottomLeft')
    else:
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='n_neighbors')],
    required_resource_keys={'pyspark'}
)
def KNeighborsClassifier(context, n_neighbors) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.neighbors import KNeighborsClassifier as LKNeighborsClassifier
        
        model = LModeling(context.run_id, LKNeighborsClassifier(n_neighbors=int(n_neighbors)),
                          model_name='KNeighborsClassifier')

        yield Output([model, []], 'BottomLeft')
    else:
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='init'),
        InputDefinition(
            name='max_iter'),
        InputDefinition(
            name='n_clusters'),
        InputDefinition(
            name='n_init'),
        InputDefinition(
            name='tol')],
    required_resource_keys={'pyspark'}
)
def Kmeans(context, init, max_iter, n_clusters, n_init, tol) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.cluster import KMeans as LKMeans
        
        model = LModeling(context.run_id,
                          LKMeans(init=init, max_iter=max_iter, n_clusters=n_clusters, n_init=n_init, tol=tol),
                          model_name='Kmeans')
        # model.fit(df)
        # tasks.append(model)
        yield Output([model, []], 'BottomLeft')
    else:
        # pre=HPre_Modeling(inputCol='y_index')
        # model=HModeling(inputCol='y_index', model=model)
        # pipe=Pipeline(stages=[pre, model]).fit(df)
        # tasks.append(pipe)
        # if context.resources.light:
        #     PipelineModel(stages=tasks).write().overwrite().save('/tmp/test')
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='n_estimators')],
    required_resource_keys={'pyspark'}
)
def RandomForestClassifier(context, n_estimators) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.ensemble import RandomForestClassifier as LRandomForestClassifier
        
        model = LModeling(context.run_id, LRandomForestClassifier(n_estimators=n_estimators),
                          model_name='RandomForestClassifier')
        # model.fit(df)
        # tasks.append(model)
        yield Output([model, []], 'BottomLeft')
    else:
        # pre=HPre_Modeling(inputCol='y_index')
        # model=HModeling(inputCol='y_index', model=model)
        # pipe=Pipeline(stages=[pre, model]).fit(df)
        # tasks.append(pipe)
        # if context.resources.light:
        #     PipelineModel(stages=tasks).write().overwrite().save('/tmp/test')
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='criterion'),
        InputDefinition(
            name='min_samples_leaf'),
        InputDefinition(
            name='min_samples_split'),
        InputDefinition(
            name='n_estimators'),
        InputDefinition(
            name='random_state')],
    required_resource_keys={'pyspark'}
)
def RandomForestRegressor(context, criterion, min_samples_leaf, min_samples_split, n_estimators,
                          random_state) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.ensemble import RandomForestRegressor as LRandomForestRegressor
        
        model = LModeling(context.run_id, LRandomForestRegressor(criterion=criterion, min_samples_leaf=min_samples_leaf,
                                                                 min_samples_split=min_samples_split,
                                                                 n_estimators=n_estimators, random_state=random_state),
                          model_name='RandomForestRegressor')
        yield Output([model, []], 'BottomLeft')
    else:
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='activation'),
        InputDefinition(
            name='alpha'),
        InputDefinition(
            name='hidden_layer_sizes'),
        InputDefinition(
            name='learning_rate'),
        InputDefinition(
            name='learning_rate_init'),
        InputDefinition(
            name='max_iter'),
        InputDefinition(
            name='solver'),
        InputDefinition(
            name='random_state')],
    required_resource_keys={'pyspark'}
)
def MultilayerPerceptronClassifier(context, activation, alpha, hidden_layer_sizes, learning_rate, learning_rate_init,
                                   max_iter, solver, random_state) -> PipelineType:
    if not context.mode_def.name == 'heavy':
        from sklearn.neural_network import MLPClassifier as LMLPClassifier
        
        model = LModeling(context.run_id,
                          LMLPClassifier(activation=activation, alpha=alpha, hidden_layer_sizes=hidden_layer_sizes,
                                         learning_rate=learning_rate, learning_rate_init=learning_rate_init,
                                         max_iter=max_iter, solver=solver, random_state=random_state),
                          model_name='MultilayerPerceptronClassifier')
        # model.fit(df)
        # tasks.append(model)
        yield Output([model, []], 'BottomLeft')
    else:
        yield Output([None, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=DataFrame
        ),
    ],
    input_defs=[InputDefinition(
        name='TopRight', dagster_type=DataFrame),
        InputDefinition(
            name='TopLeft', dagster_type=PipelineType),
        InputDefinition(
            name='label_column', dagster_type=str
        )],
    required_resource_keys={'pyspark'}
)
def RunModel(context, TopRight: DataFrame, TopLeft: PipelineType, label_column: str) -> DataFrame:
    tasks = list.copy(TopLeft[1])
    model = TopLeft[0]
    df = TopRight[0]

    if not context.mode_def.name == 'heavy':
        pred = model.transform(df.drop(label_column, axis=1))

        if model.get_model_type() == 'Classifier' and len(model.model.classes_) == 2:
            proba = model.predict_proba(df.drop(label_column, axis=1))
            df['prediction_probs'] = proba[:, 1]
        df['predictions'] = pred

        yield Output([df, tasks], 'BottomLeft')
    else:
        df = TopLeft.withColumn("predictions", model.predict(df))
        # if context.resources.light:
        #     PipelineModel(stages=tasks).write().overwrite().save('/tmp/test')
        yield Output([df, tasks], 'BottomLeft')


@solid(
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame),
        InputDefinition(
            name='label_column'),
        InputDefinition(
            name='predict_column')],
    required_resource_keys={'pyspark'}
)
def ClassificationMetrics(context, TopLeft: DataFrame, label_column, predict_column):
    df = TopLeft[0]
    if not context.mode_def.name == 'heavy':
        from tasks.light import classification_metrics
        with open("/tmp/dagster/{id}/{id}_{task_name}_eval_metrics_meta_data.json".format(id=context.run_id,
                                                                                          task_name=context.solid.name),
                  'w') as metrics_file:
            metrics = classification_metrics(df, label_column=label_column, target_column=predict_column,
                                             plot_path="/tmp/dagster/{id}/{id}_{task_name}_roc.html".format(
                                                 id=context.run_id,
                                                 task_name=context.solid.name))
            json.dump(metrics,
                      metrics_file)
        return metrics
    else:
        pipe = None
        return pipe


@solid(
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame),
        InputDefinition(
            name='label_column'),
        InputDefinition(
            name='predict_column')],
    required_resource_keys={'pyspark'}
)
def RegressionMetrics(context, TopLeft: DataFrame, label_column, predict_column):
    df = TopLeft[0]
    if not context.mode_def.name == 'heavy':
        from tasks.light import regression_metrics
        with open("/tmp/dagster/{id}/{id}_{task_name}_eval_metrics_meta_data.json".format(id=context.run_id,
                                                                                          task_name=context.solid.name),
                  'w') as metrics_file:

            metrics = regression_metrics(df, label_column=label_column, target_column=predict_column,
                                         plot_path="/tmp/dagster/{id}/{id}_{task_name}_roc.html".format(
                                             id=context.run_id,
                                             task_name=context.solid.name))
            json.dump(metrics,
                      metrics_file)
        return metrics
    else:
        pipe = None
        return pipe


# the first solids

@solid(
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame),
        InputDefinition(
            name='label_column'),
        InputDefinition(
            name='predict_column')],
    required_resource_keys={'pyspark'}
)
def ClusteringMetrics(context, TopLeft: DataFrame, label_column, predict_column):
    return RegressionMetrics(context, DataFrame, label_column, predict_column)


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='tree_method')],
    required_resource_keys={'pyspark'}
)
def XGBRegressor(context, tree_method) -> PipelineType:
    from sklearn.metrics import mean_absolute_error
    
    model = LModeling(context.run_id, xgb.XGBRegressor(
        tree_method=tree_method,
        eval_metric=mean_absolute_error,
    ), model_name='XGBRegressor')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='booster')],
    required_resource_keys={'pyspark'}
)
def XGBClassifier(context, booster) -> PipelineType:
    
    model = LModeling(context.run_id, xgb.XGBClassifier(
        booster=booster
    ), model_name='XGBClassifier')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='random_state')],
    required_resource_keys={'pyspark'}
)
def LGBMClassifier(context, random_state) -> PipelineType:
    from lightgbm import LGBMClassifier
    model = LModeling(context.run_id, LGBMClassifier(learning_rate=0.09, max_depth=3, random_state=random_state),
                      model_name='LGBMClassifier')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='num_leaves'),
        InputDefinition(name='learning_rate'),
        InputDefinition(name='n_estimators')
    ],
    required_resource_keys={'pyspark'}
)
def LGBMRegressor(context, num_leaves, learning_rate, n_estimators) -> PipelineType:
    from lightgbm import LGBMRegressor
    model = LModeling(context.run_id, LGBMRegressor(num_leaves=31, learning_rate=0.05, n_estimators=20),
                      model_name='LGBMRegressor')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(name='iterations'), InputDefinition(name='task_type')],
    required_resource_keys={'pyspark'}
)
def CatBoost(context, iterations, task_type) -> PipelineType:
    from catboost import CatBoostClassifier
    model = LModeling(context.run_id,
                      CatBoostClassifier(iterations=iterations, learning_rate=1, depth=2, task_type="CPU"),
                      model_name='CatBoost')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='algorithm')],
    required_resource_keys={'pyspark'}
)
def Adaboost(context, algorithm) -> PipelineType:
    from sklearn.ensemble import AdaBoostClassifier
    
    model = LModeling(context.run_id, AdaBoostClassifier(
        base_estimator=None,
        n_estimators=50,
        learning_rate=1.,
        algorithm=algorithm,
        random_state=None
    ), model_name='Adaboost')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='n_estimators'),
        InputDefinition(name='max_features')
    ],
    required_resource_keys={'pyspark'}
)
def BaggingClassifier(context, n_estimators, max_features) -> PipelineType:
    from sklearn.ensemble import BaggingClassifier
    

    model = LModeling(context.run_id,
                      BaggingClassifier(n_estimators=n_estimators, max_samples=10, max_features=max_features),
                      model_name='BaggingClassifier')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='epochs'),

    ],
    required_resource_keys={'pyspark'}
)
def LSTM_Model(context, epochs):
    
    model = LModeling(context.run_id, LSTM(epochs=epochs), model_name='LSTM_Model')
    yield Output([model, []], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='label_column'
    ), InputDefinition(
        name='pca_components'
    )
    ],
)
def PCA_PC(context, TopLeft: DataFrame, label_column, pca_components):
    from pycaret.classification import setup, get_config
    df = TopLeft[0]
    df = setup(data=df, target=label_column, pca=True, pca_components=pca_components, silent=True)
    df_pca = pd.DataFrame(get_config('X'))
    df_pca[label_column] = get_config('y')
    yield Output([df_pca, []], 'BottomLeft')


@solid(
    output_defs=[OutputDefinition(
        name='BottomLeft', dagster_type=DataFrame
    )],
    input_defs=[InputDefinition(
        name='TopLeft', dagster_type=DataFrame
    ), InputDefinition(
        name='label_column'
    ),
    ],
)
def ILV_PC(context, TopLeft: DataFrame, label_column):
    from pycaret.classification import setup, get_config
    df = TopLeft[0]
    df = setup(data=df, target=label_column, ignore_low_variance=True, silent=True)
    df_pca = pd.DataFrame(get_config('X'))
    df_pca[label_column] = get_config('y')
    yield Output([df_pca, []], 'BottomLeft')


@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[InputDefinition(
        name='learning_rate'),

    ],
    required_resource_keys={'pyspark'}
)
def SGDC_Calissifier(context, learning_rate):
    from sklearn.linear_model import SGDClassifier
    
    model = LModeling(context.run_id, SGDClassifier(alpha=0.0001, class_weight=None, epsilon=0.1, eta0=0.0,
                                                    fit_intercept=True, l1_ratio=0.15, learning_rate=learning_rate,
                                                    loss='hinge', n_jobs=1, penalty='l2', power_t=0.5,
                                                    random_state=None, shuffle=False,
                                                    verbose=0, warm_start=False), model_name='SGDC_Calissifier',
                      fl=True)
    yield Output([model, []], 'BottomLeft')
@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='alpha'),
        InputDefinition(name='fit_prior'),
    ],
    required_resource_keys={'pyspark'}
)
def MultinomialNB_Classifier(context, alpha=1.0,fit_prior=True):
    # learning_rate = 'optimal'
    from sklearn.naive_bayes import MultinomialNB
    
    model = LModeling(context.run_id, MultinomialNB(alpha=alpha, fit_prior=fit_prior), model_name='MultinomialNB_Classifier',
                      fl=True)
    yield Output([model, []], 'BottomLeft')
@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='alpha'),
        InputDefinition(name='fit_prior'),

    ],
    required_resource_keys={'pyspark'}
)
def BernoulliNB_Classifier(context, alpha=1.0,fit_prior=True):
    # learning_rate = 'optimal'
    from sklearn.naive_bayes import BernoulliNB
    
    model = LModeling(context.run_id, BernoulliNB(alpha=alpha,fit_prior=fit_prior), model_name='BernoulliNB_Classifier',
                      fl=True)
    yield Output([model, []], 'BottomLeft')
@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='penalty'),
        InputDefinition(name='alpha'),
        InputDefinition(name='fit_intercept'),

    ],
    required_resource_keys={'pyspark'}
)
def Perceptron_Classifier(context, penalty=None,alpha=0.0001,fit_intercept=True):
    # penalty None,l2,l1
    # learning_rate = 'optimal'
    from sklearn.linear_model import Perceptron
    
    model = LModeling(context.run_id, Perceptron(penalty=penalty,alpha=alpha,fit_intercept=True), model_name='Perceptron_Classifier',
                      fl=True)
    yield Output([model, []], 'BottomLeft')

@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='step_size'),
        InputDefinition(name='fit_intercept'),

    ],
    required_resource_keys={'pyspark'}
)
def PassiveAggressive_Classifier(context, step_size=1.0, fit_intercept=True):
    # learning_rate = 'optimal'
    from sklearn.linear_model import PassiveAggressiveClassifier
    
    model = LModeling(context.run_id, PassiveAggressiveClassifier(C=step_size,fit_intercept=fit_intercept), model_name='PassiveAggressive_Classifier',
                      fl=True)
    yield Output([model, []], 'BottomLeft')

@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='step_size'),
        InputDefinition(name='epsilon'),
        InputDefinition(name='fit_intercept'),

    ],
    required_resource_keys={'pyspark'}
)
def PassiveAggressive_Regressor(context, step_size=1.0,epsilon=0.1,fit_intercept=True):
    # learning_rate = 'optimal'
    from sklearn.linear_model import PassiveAggressiveRegressor
    
    model = LModeling(context.run_id, PassiveAggressiveRegressor(C=step_size,epsilon=epsilon,fit_intercept=fit_intercept), model_name='PassiveAggressive_Regressor',
                      fl=True)
    yield Output([model, []], 'BottomLeft')

@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='n_clusters'),
        InputDefinition(name='num_iter'),

    ],
    required_resource_keys={'pyspark'}
)
def MiniBatchKMeans(context, n_clusters=8,num_iter=100):
    # learning_rate = 'optimal'
    from sklearn.cluster import MiniBatchKMeans
    model = LModeling(context.run_id, MiniBatchKMeans(n_clusters=n_clusters,num_iter=num_iter), model_name='MiniBatchKMeans',
                      fl=True)
    yield Output([model, []], 'BottomLeft')

@solid(
    output_defs=[
        OutputDefinition(
            name='BottomLeft', dagster_type=PipelineType
        ),
    ],
    input_defs=[
        InputDefinition(name='model_name'),
    ],
    required_resource_keys={'pyspark'}
)
def PreTrainedModel(context, model_name):
    # this basically loads a pkl
    loaded_model = get_deployed_wf_model(model_name)
    loaded_model.model_name=model_name
    model = LModeling(context.run_id, loaded_model, model_name='PreTrainedModel', fl=True)
    yield Output([model, []], 'BottomLeft')