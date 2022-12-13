from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer as Imputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from collections import defaultdict
import sqlite3
import pandas as pd
import numpy as np
import ast
import imblearn.over_sampling as imbl_os
import imblearn.under_sampling as imbl_us
from sklearn.metrics import f1_score, recall_score, average_precision_score, accuracy_score, confusion_matrix, r2_score, mean_absolute_error, mean_squared_error
from dagster_resources import engine_config as conf
from tasks.ml_menu_generator import get_model_type
from dagster_resources import object_storage_handler as osh
# from sklearn.externals \

USER_MODELS_ = "./user/models/"
__outputs_path = conf.FS_HANDLER_CONFIG['outputs_path']

##################################### Sklearn-TASKS #####################################

class LSelectColumns(TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name.split(',')

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        return x.filter(items=self.col_name)


class LDropMissing(BaseEstimator, TransformerMixin):
    """
    Task Name: Drop Missing Records
    DESC: Drop missing records from a row or column
    Task Parameters:
        - Drop Type: Drop row with missing, drop empty rows, drop empty columns
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with no missing records
    """

    def __init__(self, drop):
        self.drop_type = drop

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        if self.drop_type == 'DROP_ROW_WITH_MISSING':
            x.dropna(axis=0, inplace=True)
        elif self.drop_type == 'DROP_EMPTY_ROW':
            x.dropna(axis=0, how='all', inplace=True)
        elif self.drop_type == 'DROP_EMPTY_COLUMN':
            x.dropna(axis=1, how='all', inplace=True)
        return x


class LApplySqlite(BaseEstimator, TransformerMixin):
    """
    Task Name: Apply Sqlite
    DESC: Returns a DataFrame corresponding to the result set of the query string.
    Task Parameters:
        -SQL query: string SQL query
    Task Inputs:
        - Input1: a Data frame
        - Input2: a Data frame (optional)
    Task Outputs:
        - Output1: a Data frame with the applied SQL query
    """

    def __init__(self, query):
        self.sqlite_query = query

    def fit(self, x, y=None):
        return self

    def transform(self, x1, x2, y=None):
        temp_db_conn = sqlite3.connect('')

        x1.to_sql('TopLeft', temp_db_conn, if_exists='replace')
        del x1

        if x2 is not None:
            x2.to_sql('TopRight', temp_db_conn, if_exists='replace')
            del x2

        result_df = pd.read_sql_query(self.sqlite_query, temp_db_conn)

        temp_db_conn.close()

        return result_df


class LJoinData(BaseEstimator, TransformerMixin):
    """
    Task Name: Join Data
    DESC: Merge Data frame objects by performing a database-style join operation.
    Task Parameters:
        - Left column name: Field names to join on in left data frame
        - Right column name: Field names to join on in right data frame
        - Join Type: Type of join to apply
    Task Inputs:
        - Input1: a Data frame
        - Input2: a Data frame
    Task Outputs:
        - Output1: a Data frame with join applied
    """

    def __init__(self, left_col, right_col, join_type):
        self.left_col_names = left_col
        self.right_col_names = right_col
        self.join_type = join_type

    def fit(self, x, y=None):
        return self

    def transform(self, df1: pd.DataFrame, df2: pd.DataFrame):
        try:
            return pd.merge(df1, df2, left_on=str(self.left_col_names).split(','),
                        right_on=str(self.right_col_names).split(','), how=self.join_type)
        except ValueError:
            return pd.concat([df1, df2])


class LFillMissingWithMean(BaseEstimator, TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name.split(',')

    def fit(self, x, y=None):
        if self.col_name == ['all']:
            self.col_name = list(x.select_dtypes([float, int]).columns)
        self.lm_ = Imputer(strategy='mean')
        self.lm_.fit(x.loc[:, self.col_name])
        return self

    def transform(self, x, y=None):
        x.loc[:, self.col_name] = self.lm_.transform(x.loc[:, self.col_name])
        return x


class LFillMissingWithValue(BaseEstimator, TransformerMixin):
    def __init__(self, col_name, value):
        self.col_name = col_name.split(',')
        self.value = value

    def fit(self, x, y=None):
        if self.col_name == ['all']:
            self.col_name = x.select_dtypes([float, int]).columns
        self.lm_ = Imputer(strategy="constant", fill_value=ast.literal_eval(str(self.value)))
        self.lm_.fit(x.loc[:, self.col_name])
        return self

    def transform(self, x, y=None):
        x.loc[:, self.col_name] = self.lm_.transform(x.loc[:, self.col_name])
        return x


class LChangeDtypes(BaseEstimator, TransformerMixin):
    """
    Task Name: Change Data Types
    DESC: Change columns data type to selected type
    Task Parameters:
        - Column Names: name of columns with new data types to be changed
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with select columns data types changed
    """

    def __init__(self, col_name):
        self.changed_columns = col_name

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        cols = ast.literal_eval(str(self.changed_columns))

        for col_name, col_type in cols.items():
            df[col_name] = df[col_name].astype(col_type)

        return df


class LColumnBinning(BaseEstimator, TransformerMixin):
    """
    Task Name: Column Binning
    DESC: Binning selected columns with desired number of bins
    Task Parameters:
        - Column Names: name of columns to be binned
        - Number of bins: number of bins for the column
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with binned selected columns
    """

    def __init__(self, col_name, no_bins):
        self.col_name = col_name.split(',')
        self.no_bins = no_bins

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        for col in self.col_name:
            try:
                df[col + '_binned'] = pd.cut(df[col], int(self.no_bins)).astype(str)
            except TypeError:
                key = col + '_binned'
                df[key] = str(pd.cut(df[col], int(self.no_bins)))
        return df


class LReplaceValue(TransformerMixin):
    """
    Task Name: Replace Values
    DESC: Replace values given in ‘value to replace’ with ‘replacement value’ in a column
    Task Parameters:
        - Value to Replace: value to replace in a column
        - Replacement Value: value used in replacement
        - Column Names: names of the columns where replacement will take place
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with replaced values
    """

    def __init__(self, value_to_replace, replacement_value, col_names):
        self.value_to_replace = value_to_replace
        self.replacement_value = replacement_value
        self.col_names = col_names.split(',')

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        if self.col_names == ['all']:
            df.replace(self.value_to_replace, self.replacement_value, inplace=True)
        else:
            for col_name in self.col_names:
                df[col_name].replace(self.value_to_replace, self.replacement_value, inplace=True)

        return df


class LCategoryEncoding(BaseEstimator, TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name.split(',')
        self.mapping = {}

    def fitAndSaveMapping(self, x):
        value, index = np.unique(x, return_index=True)
        fitted =self.lm_[x.name].transform(x)
        aux = {}
        for i, val in enumerate(value):
            aux[val] = fitted[index[i]]
        self.mapping[x.name] = aux
        return fitted

    def fit(self, x, y=None):
        self.lm_ = defaultdict(LabelEncoder)
        x[self.col_name].apply(lambda x: self.lm_[x.name].fit(x))
        return self

    def transform(self, x, y=None):
        x.loc[:, self.col_name] = x[self.col_name].apply(lambda x: self.fitAndSaveMapping(x))
        return x


class LNormalized(BaseEstimator, TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name.split(',')

    def fit(self, x, y=None):
        self.lm_ = MinMaxScaler()
        self.lm_.fit(x[self.col_name])
        return self

    def transform(self, x, y=None):
        self.lm_.transform(x[self.col_name])
        return x


class LStandardized(BaseEstimator, TransformerMixin):
    def __init__(self, col_name):
        self.col_name = col_name.split(',')

    def fit(self, x, y=None):
        self.lm_ = StandardScaler()
        self.lm_.fit(x[self.col_name])
        return self

    def transform(self, x, y=None):
        self.lm_.transform(x[self.col_name])
        return x


class LChangeColumnsName(TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, col_name):
        self.col_name_dict = col_name

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        df.rename(columns=ast.literal_eval(str(self.col_name_dict)), inplace=True)
        return df


class LMeltingDf(TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, id_vars, value_vars):
        self.id_vars = id_vars
        self.value_vars = value_vars

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        pd.melt(frame=df, id_vars=self.id_vars, value_vars=self.value_vars)
        return df


class LCategoryToDigits(BaseEstimator, TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, col_names):
        self.col_names = col_names.split(',')

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        for col in self.col_names:
            # df[col] = pd.Categorical(df[col])
            df[col + '_to_digits'] = df[col].cat.codes
        return df


class LOverSample(TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, label_column, random_seed, over_sampling_type):
        self.label_column = label_column.split(',')
        self.random_seed = random_seed  # Must be set to -1 if not provided by the user
        self.over_sampling_type = over_sampling_type

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        rseed = None
        over_sampler = None

        if self.random_seed != -1:
            rseed = self.random_seed

        if self.over_sampling_type == 'RANDOM_OVER_SAMPLING':
            over_sampler = imbl_os.RandomOverSampler(random_state=rseed)
        elif self.over_sampling_type == 'ADASYN':
            over_sampler = imbl_os.ADASYN(random_state=rseed)
        elif self.over_sampling_type == 'SMOTE_REGULAR':
            over_sampler = imbl_os.SMOTE(random_state=rseed)
        elif self.over_sampling_type == 'SMOTE_SVM':
            over_sampler = imbl_os.SVMSMOTE(random_state=rseed)
        elif self.over_sampling_type == 'SMOTE_BORDERLINE1':
            over_sampler = imbl_os.BorderlineSMOTE(random_state=rseed, kind='borderline-1')
        elif self.over_sampling_type == 'SMOTE_BORDERLINE2':
            over_sampler = imbl_os.BorderlineSMOTE(random_state=rseed, kind='borderline-2')

        x, y = over_sampler.fit_sample(df.drop(self.label_column, axis=1), df[self.label_column])
        x[self.label_column] = y
        return x


class LUnderSample(TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, label_column, random_seed, under_sampling_type):
        self.label_column = label_column.split(',')
        self.random_seed = random_seed  # Must be set to -1 if not provided by the user
        self.under_sampling_type = under_sampling_type

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        rseed = None
        under_sampler = None

        if self.random_seed != -1:
            rseed = self.random_seed

        if self.under_sampling_type == 'RANDOM_UNDER_SAMPLING':
            under_sampler = imbl_us.RandomUnderSampler(random_state=rseed)
        elif self.under_sampling_type == 'TOMEK_LINKS':
            under_sampler = imbl_us.TomekLinks()
        elif self.under_sampling_type == 'NEIGHBOURHOOD_CLEANING_RULE':
            under_sampler = imbl_us.NeighbourhoodCleaningRule()
        elif self.under_sampling_type == 'CONDENSED_NEAREST_NEIGHBOUR':
            under_sampler = imbl_us.CondensedNearestNeighbour(random_state=rseed)
        elif self.under_sampling_type == 'EDITED_NEAREST_NEIGHBOUR':
            under_sampler = imbl_us.EditedNearestNeighbours()
        elif self.under_sampling_type == 'REPEATED_EDITED_NEAREST_NEIGHBOUR':
            under_sampler = imbl_us.RepeatedEditedNearestNeighbours()
        elif self.under_sampling_type == 'ALL_KNN':
            under_sampler = imbl_us.AllKNN()
        elif self.under_sampling_type == 'CLUSTER_CENTROIDS_SOFT_VOTING':
            under_sampler = imbl_us.ClusterCentroids(random_state=rseed)
        elif self.under_sampling_type == 'CLUSTER_CENTROIDS_HARD_VOTING':
            under_sampler = imbl_us.ClusterCentroids(random_state=rseed, voting='hard')
        elif self.under_sampling_type == 'NEARMISS_V1':
            under_sampler = imbl_us.NearMiss(version=1)
        elif self.under_sampling_type == 'NEARMISS_V2':
            under_sampler = imbl_us.NearMiss(version=2)
        elif self.under_sampling_type == 'NEARMISS_V3':
            under_sampler = imbl_us.NearMiss(version=3)
        elif self.under_sampling_type == 'ONE_SIDED_SELECTION':
            under_sampler = imbl_us.OneSidedSelection(random_state=rseed)

        x, y = under_sampler.fit_sample(df.drop(self.label_column, axis=1), df[self.label_column])
        x[self.label_column] = y

        return x


class LModeling(BaseEstimator, TransformerMixin):
    def __init__(self, run_id, model, target='y', model_name=None, fl=False):
        self.run_id = run_id
        self.model_name = model_name
        self.model = model
        self.target = target
        self.fl = fl
        try:
            self._estimator_type = model._estimator_type
        except Exception:
            self._estimator_type = 'classifier'
        self._label_name = target

    def save(self):
        # fileName = USER_MODELS_ + str(self.model_name) + ".pkl"
        # with open(fileName, "wb") as f:
        #     pickle.dump(self.model, f)
        #     print("done; "+fileName)
        res = osh.put_deployed_wf_model(self.model, self.run_id+"_"+self.model_name)
        print(res)

    def fit(self, x, y=None):
        if self.fl:
            print("we are cooking FL")
            self.model.partial_fit(x, y, classes=np.unique(y))
        else:
            self.model.fit(x, y)

        return self

    def predict_proba(self, x, y=None):
        try:
            return self.model.predict_proba(x)
        except AttributeError:
            guys = ['Perceptron_Classifier', 'Perceptron_Classifier', 'Perceptron_Classifier']
            if self.model_name in guys:
                aux = self.model.decision_function(x).flatten()
                aux1 = np.array_repr(aux, precision=6, suppress_small=True)
                return aux1

    def transform(self, x, y=None):
        try:
            return self.model.predict(x)
        except Exception:
            from torch import Tensor
            row = Tensor([x.values])
            row.unsqueeze_(0)
            self.model(row)
            print()

    def score(self, x, y=None):
        return self.model.score(x, y)

    def set_label(self, target):
        self._label_name = target

    def get_model_name(self):
        return self.model_name

    def get_model_type(self):
        return get_model_type(self.model_name)


def generate_roc_HTML_chart(label_column, preds_prob, plot_path):
    import plotly.graph_objs as go
    import plotly
    import matplotlib.pyplot as plt
    from sklearn import metrics as mt
    fpr, tpr, threshold = mt.roc_curve(label_column, preds_prob)
    plt.roc_auc = mt.auc(fpr, tpr)
    roc_auc = mt.auc(fpr, tpr)

    trace1 = go.Scatter(x=fpr, y=tpr, name='AUC = %0.2f' % roc_auc, showlegend=True)
    trace2 = go.Scatter(x=[0, 1], y=[0, 1], line=dict(color='rgb(205,12,24)', dash='dash'), showlegend=False)
    layout = dict(title='ROC Curve', xaxis=dict(title='True Positive Rate'), yaxis=dict(title='Flase Positive Rate'),
                  height=400, width=670, autosize=False)
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    plotly.offline.plot(fig, filename=plot_path, show_link=False, auto_open=False,
                        include_plotlyjs=False)

    return plot_path


def classification_metrics(df, label_column, target_column, plot_path):
    # metrics
    try:
        probs = df['prediction_probs']
    except Exception:
        probs = df['predictions']

    generate_roc_HTML_chart(df[label_column], probs, plot_path)

    accuracy = accuracy_score(df[label_column], df[target_column])
    # classification = classification_report(df[label_column], df[target_column])
    try:
        tn, fp, fn, tp = confusion_matrix(df[label_column], df[target_column]).ravel()
    except ValueError:
        theVal = confusion_matrix(df[label_column], df[target_column]).ravel()

    f1 = f1_score(df[label_column], df[target_column], average=None).tolist()
    recall = recall_score(df[label_column], df[target_column], average=None).tolist()
    precision_score = average_precision_score(df[label_column], df[target_column], average=None)

    metrics_dict = {'accuracy_score': accuracy,
                    'f1_score': f1, 'recall_score': recall, 'precision_score': precision_score,
                    'tn': tn.item(), 'fp': fp.item(), 'fn': fn.item(), 'tp': tp.item(),
                    'model_type': 'classification'}

    return metrics_dict


class LClassificationMetrics(TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, label_column, predict_column):
        self.label_column = label_column
        self.predict_column = predict_column

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        metrics = classification_metrics(df, self.label_column, self.predict_column,
                                         "/tmp/dagster/{id}/{id}_{task_name}_roc.html")
        return metrics


def generate_regression_plot(df, label_column, target_column, plot_path):
    import plotly.graph_objs as go
    import plotly
    from plotly import subplots

    try:
        df = df.sample(n=100)
    except ValueError:
        df = df.sample(n=100, replace=True)

    trace1 = go.Scatter(x=df[label_column], y=df[target_column], mode='markers', showlegend=False)
    trace2 = go.Scatter(x=df[target_column], y=df[label_column] - df[target_column], mode='markers', showlegend=False)

    fig = subplots.make_subplots(rows=2, cols=1, subplot_titles=('Actual vs Predicted', 'Residuals vs Fitted'))

    fig.add_trace(trace1, 1, 1)
    fig.add_trace(trace2, 2, 1)

    fig['layout']['xaxis1'].update(title=label_column.capitalize())
    fig['layout']['xaxis2'].update(title='Fitted Values')

    fig['layout']['yaxis1'].update(title=target_column.capitalize())
    fig['layout']['yaxis2'].update(title='Residuals')
    fig['layout'].update(height=800, width=670)

    plotly.offline.plot(fig, filename=plot_path, show_link=False, auto_open=False, include_plotlyjs=False)

    return plot_path


def regression_metrics(df, label_column, target_column, plot_path):
    # metrics
    try:
        m_absolute_error = mean_absolute_error(df[label_column], df[target_column])
    except ValueError:
        import numpy as np
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        m_absolute_error = mean_absolute_error(df[label_column], df[target_column])

    m_squared_error = mean_squared_error(df[label_column], df[target_column])
    r2 = r2_score(df[label_column], df[target_column])

    metrics_dict = {'mean_absolute_error': m_absolute_error, 'mean_squared_error': m_squared_error,
                    'r2_score': r2, 'model_type': 'regression'}
    # metrics_df = pd.DataFrame(metrics_dict)
    # elmdptt.generate_actual_vs_predicted_pairwise_HTML_chart(df, label_column, target_column, plot_path)
    # elmdptt.generate_residuals_HTML_chart(df, label_column, target_column, plot_path)
    generate_regression_plot(df, label_column, target_column, plot_path)
    # all_plots = actual_vs_predicted_scatter + resid_scatter

    return metrics_dict


class LRegressionMetrics(TransformerMixin):
    """
    Task Name: Change Columns Names
    DESC:Renames selected columns
    Task Parameters:
        - Column Names: selected columns to be renames
        - New names: new column names
    Task Inputs:
        - Input1: a Data frame
    Task Outputs:
        - Output1: a Data frame with columns renamed
    """

    def __init__(self, label_column, predict_column):
        self.label_column = label_column
        self.predict_column = predict_column

    def fit(self, x, y=None):
        return self

    def transform(self, df: pd.DataFrame):
        return regression_metrics(df, self.label_column, self.predict_column)

#####################################  END  #####################################
