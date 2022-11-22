from pyspark.ml import Pipeline,PipelineModel, Transformer,Estimator
from pyspark.sql import SparkSession, functions as F
from pyspark import keyword_only, SparkContext, SparkConf, SQLContext
from pyspark.ml.param.shared import HasInputCols, HasInputCol, HasOutputCols, HasOutputCol, Param, Params
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel, RandomForestClassifier as rfc
from pyspark.ml.feature import Binarizer,VectorAssembler, StringIndexer, Imputer as SImputer
from pyspark.mllib.evaluation import MulticlassMetrics, BinaryClassificationMetrics
##################################### TASKS #####################################

class HSelectColumns(
    Transformer, DefaultParamsReadable, DefaultParamsWritable,
):
    columns = Param(
        Params._dummy(),
        "columns",
        "columns",
    )

    @keyword_only
    def __init__(self, columns=None):
        super(HSelectColumns, self).__init__()
        self._setDefault(columns=None)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @keyword_only
    def setParams(self, columns=None):
        """
        setParams(self, outputCols=None, value=0.0)
        Sets params for this SetMeanImputer.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setValue(self, columns=None):
        """
        Sets the value of :py:attr:`value`.
        """
        return self._set(columns=columns)

    def getValue(self):
        """
        Gets the value of :py:attr:`value` or its default value.
        """
        return self.getOrDefault(self.columns)

    def _transform(self, df):
        return df.select(*self.getValue())

class HDropColumn(
    Transformer, DefaultParamsReadable, DefaultParamsWritable,
):
    columns = Param(
        Params._dummy(),
        "columns",
        "columns",
    )

    @keyword_only
    def __init__(self, columns=None):
        super(HDropColumn, self).__init__()
        self._setDefault(columns=None)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @keyword_only
    def setParams(self, columns=None):
        """
        setParams(self, outputCols=None, value=0.0)
        Sets params for this SetMeanImputer.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setValue(self, columns=None):
        """
        Sets the value of :py:attr:`value`.
        """
        return self._set(columns=columns)

    def getValue(self):
        """
        Gets the value of :py:attr:`value` or its default value.
        """
        return self.getOrDefault(self.columns)

    def _transform(self, df):
        return df.drop(*self.getValue())


class HFillMissingWithMean(
    Estimator, HasInputCol, HasInputCols, HasOutputCols, DefaultParamsReadable, DefaultParamsWritable,
):
    model = Param(
        Params._dummy(),
        "model",
        "model",
    )

    @keyword_only
    def __init__(self, inputCols=None, model=None):
        super(HFillMissingWithMean, self).__init__()
        self._setDefault(model=None)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @keyword_only
    def setParams(self, model=None):
        """
        setParams(self, model=0.0)
        Sets params for this SetMeanImputer.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setValue(self, model):
        """
        Sets the value of :py:attr:`value`.
        """
        return self._set(model=model)

    def getValue(self):
        """
        Gets the value of :py:attr:`value` or its default value.
        """
        return self.getOrDefault(self.model)

    def transform(self, df):
        return self.getValue().transform(df)

    #         return ImputerModel.load("pipes/"+self.getValue()).transform(df)

    def _fit(self, df):
        if self.getInputCols() == ['all']:
            lm = SImputer(inputCols=df.columns,
                        outputCols=df.columns, strategy='mean')
            model = lm.fit(df)
        else:
            col = self.getInputCols()
            lm = SImputer(inputCols=col,
                        outputCols=col, strategy='mean')
            model = lm.fit(df)
        #         name=str(model)
        #         model.write().overwrite().save("pipes/"+name)
        return model


class HCategoryEncoding(
    Estimator, HasInputCols, HasOutputCols, DefaultParamsReadable, DefaultParamsWritable,
):
    model = Param(
        Params._dummy(),
        "model",
        "model",
    )

    @keyword_only
    def __init__(self, inputCols=None, model=None):
        super(HCategoryEncoding, self).__init__()
        self._setDefault(model=None)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @keyword_only
    def setParams(self, model=None):
        """
        setParams(self, model=0.0)
        Sets params for this SetMeanImputer.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setValue(self, model):
        """
        Sets the value of :py:attr:`value`.
        """
        return self._set(model=model)

    def getValue(self):
        """
        Gets the value of :py:attr:`value` or its default value.
        """
        return self.getOrDefault(self.model)

    #     def transform(self, df):
    #         return self.getValue().transform(df)
    #         return PipelineModel.load("pipes/"+self.getValue()).transform(df).drop('v')

    def _fit(self, df):
        if isinstance(self.getInputCols(), str):
            self.setInputCols([*self.getInputCols()])

        indexers = [StringIndexer(inputCol=column, outputCol=column + "_index").fit(df) for column in
                    list(set(self.getInputCols()))]

        indexers_pipe = Pipeline(stages=indexers+[HDropColumn(columns=self.getInputCols())])
        model = indexers_pipe.fit(df)
        #         name=str(indexers_pipe)
        #         model.write().overwrite().save("pipes/"+name)
        return model


class HSplitData(
    Transformer, HasInputCol, DefaultParamsReadable, DefaultParamsWritable
):
    perc = Param(
        Params._dummy(),
        "perc",
        "perc",
    )

    @keyword_only
    def __init__(self, perc=None, inputCol=None):
        super(HSplitData, self).__init__()
        self._setDefault(perc=None)
        self._setDefault(inputCol=None)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @keyword_only
    def setParams(self, perc=None):
        """
        setParams(self, outputCols=None, value=0.0)
        Sets params for this SetMeanImputer.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setValue(self, perc=None):
        """
        Sets the value of :py:attr:`value`.
        """
        return self._set(perc=perc)

    def getValue(self):
        """
        Gets the value of :py:attr:`value` or its default value.
        """
        return self.getOrDefault(self.perc)

    def _transform(self, df):
        perc = self.getValue()
        train, test = df.randomSplit([perc, 1 - perc], seed=42)
        if self.getInputCol()=='train':
            return train
        elif self.getInputCol()=='test':
            return test
        return train, test


class HPre_Modeling(
    Transformer, HasInputCol, DefaultParamsReadable, DefaultParamsWritable,
):

    @keyword_only
    def __init__(self, inputCol=None):
        super(HPre_Modeling, self).__init__()
        kwargs = self._input_kwargs
        self._set(**kwargs)

    def _transform(self, df):
        Bin = Binarizer(threshold=0.0, inputCol=self.getInputCol(), outputCol="label")
        train = Bin.transform(df).drop(self.getInputCol())
        features = train.drop('label').columns
        assembler = VectorAssembler(inputCols=features, outputCol="features")
        train = assembler.transform(train)
        return train


class HModeling(
    Estimator, HasInputCol, HasOutputCols, DefaultParamsReadable, DefaultParamsWritable,
):
    model = Param(
        Params._dummy(),
        "model",
        "model",
    )

    @keyword_only
    def __init__(self, inputCol=None, model=None):
        super(HModeling, self).__init__()
        self._setDefault(model=None)
        kwargs = self._input_kwargs
        self._set(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, model=None):
        """
        setParams(self, model=0.0)
        Sets params for this SetMeanImputer.
        """
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setModel(self, model):
        """
        Sets the value of :py:attr:`value`.
        """
        return self._set(model=model)

    def getModel(self):
        """
        Gets the value of :py:attr:`value` or its default value.
        """
        return self.getOrDefault(self.model)

    def getParams(self):
        return self.getOrDefault(self.params)

    def transform(self, df):
        pass

    def _fit(self, df):
        if type(df) == tuple:
            df = df[0]

        rfc = eval(self.getModel())
        model = rfc.fit(df)
        return model


class HClassificationMetrics(
    Transformer, DefaultParamsReadable, DefaultParamsWritable,
):
    def _transform(self, df):
        if type(df) == tuple:
            train = df[0]
            test = df[1]
        else:
            test = df

        metrics = MulticlassMetrics(test.select('label', 'prediction').rdd.map(tuple))
        accuracy = metrics.accuracy
        #     classification = metrics.
        #     tn, fp, fn, tp = sklearn.metrics.confusion_matrix(df[label_column], df[target_column]).ravel()
        f1_score = metrics.fMeasure()
        recall_score = metrics.recall()
        precision_score = metrics.precision()
        metrics_dict = {'accuracy_score': accuracy,
                        'f1_score': f1_score, 'recall_score': recall_score, 'precision_score': precision_score,
                        'model_type': 'classification'}
        #     # metrics_df = pd.DataFrame(metrics_dict)
        return metrics_dict
##################################### END OF TASKS #####################################
