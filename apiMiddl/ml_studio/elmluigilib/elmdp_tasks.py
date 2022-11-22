import machine_learning_app.elmluigilib.elmdp_template_tasks as elmdptt
import machine_learning_app.elmluigilib.elmdp_enumerations as elmdpenum
import pandas as pd
import luigi
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import sqlite3
import imblearn.over_sampling as imbl_os
import imblearn.under_sampling as imbl_us
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import tree
import ast
from sklearn.cluster import KMeans

_data_path = '/home/admin/luigi_outputs/'


# Tasks
class ReadCSV(elmdptt.TaskNoneToOne):
    csv_path = luigi.Parameter()

    def actual_task_code(self):
        return pd.read_csv(_data_path + self.csv_path)


class SplitData(elmdptt.TaskOneToTwo):
    partition_percentage = luigi.FloatParameter()

    def actual_task_code(self, df: pd.DataFrame):
        split_1, split_2 = train_test_split(df, test_size=self.partition_percentage)
        return split_1, split_2


class RowFilter(elmdptt.TaskOneToOne):
    filter_expression = luigi.Parameter()

    def actual_task_code(self, df: pd.DataFrame):
        df.query(str(self.filter_expression), inplace=True)
        return df


class SelectColumns(elmdptt.TaskOneToOne):
    col_names = luigi.Parameter()  # Must be formatted like 'c1,c2,c3'

    def actual_task_code(self, df: pd.DataFrame):
        result_df = df.filter(items=str(self.col_names).split(','))
        return result_df


class DropMissing(elmdptt.TaskOneToOne):
    drop_type = luigi.EnumParameter(enum=elmdpenum.DropMissingTypes)

    def actual_task_code(self, df: pd.DataFrame):
        if self.drop_type is elmdpenum.DropMissingTypes.DROP_ROW_WITH_MISSING:
            df.dropna(inplace=True)
        elif self.drop_type is elmdpenum.DropMissingTypes.DROP_EMPTY_ROW:
            df.dropna(how='all', inplace=True)
        elif self.drop_type is elmdpenum.DropMissingTypes.DROP_EMPTY_COLUMN:
            df.dropna(axis=1, how='all', inplace=True)

        return df


class ApplySqlite(elmdptt.TaskTwoToOne):
    sqlite_query = luigi.Parameter()

    def actual_task_code(self, df1: pd.DataFrame, df2: pd.DataFrame):
        temp_db_conn = sqlite3.connect('')

        df1.to_sql('df1', temp_db_conn, if_exists='replace')
        del df1

        if df2 is not None:
            df2.to_sql('df2', temp_db_conn, if_exists='replace')
            del df2

        result_df = pd.read_sql_query(self.sqlite_query, temp_db_conn)

        temp_db_conn.close()

        return result_df


class JoinData(elmdptt.TaskTwoToOne):
    left_col_names = luigi.Parameter()  # Must be formatted like 'c1,c2,c3'
    right_col_names = luigi.Parameter()  # Must be formatted like 'c1,c2,c3'
    join_type = luigi.EnumParameter(enum=elmdpenum.JoinDataTypes)

    def actual_task_code(self, df1: pd.DataFrame, df2: pd.DataFrame):
        return pd.merge(df1, df2, left_on=str(self.left_col_names).split(','),
                             right_on=str(self.right_col_names).split(','), how=self.join_type.value)



class ReplaceValue(elmdptt.TaskOneToOne):
    value_to_replace = luigi.Parameter()
    replacement_value = luigi.Parameter()
    col_names = luigi.Parameter()  # Must be formatted like 'c1,c2,c3'

    def actual_task_code(self, df: pd.DataFrame):
        if self.col_names == 'all':
            df.replace(self.value_to_replace, self.replacement_value, inplace=True)
        else:
            for col_name in str(self.col_names).split(','):
                df[col_name].replace(self.value_to_replace, self.replacement_value, inplace=True)

        return df


class FillMissingWithMean(elmdptt.TaskOneToOne):
    col_names = luigi.Parameter()  # Must be formatted like 'c1,c2,c3'

    def actual_task_code(self, df: pd.DataFrame):
        if self.col_names == 'all':
            df.fillna(df.mean(), inplace=True)
        else:
            for col_name in str(self.col_names).split(','):
                df[col_name].fillna(df[col_name].mean(), inplace=True)

        return df


class FillMissingWithValue(elmdptt.TaskOneToOne):
    replacement_value = luigi.Parameter()
    col_names = luigi.Parameter()  # Must be formatted like 'c1,c2,c3'

    def actual_task_code(self, df: pd.DataFrame):
        if self.col_names == 'all':
            df.fillna(self.replacement_value, inplace=True)
        else:
            for col_name in str(self.col_names).split(','):
                df[col_name].fillna(self.replacement_value, inplace=True)

        return df


class ChangeDtypes(elmdptt.TaskOneToOne):
    changed_columns = luigi.Parameter()

    def actual_task_code(self, df: pd.DataFrame):
        cols = ast.literal_eval(self.changed_columns)

        for col_name, col_type in cols.items():
            df[col_name] = df[col_name].astype(col_type)

        return df


class OverSample(elmdptt.TaskOneToOne):
    label_column = luigi.Parameter()
    random_seed = luigi.IntParameter()  # Must be set to -1 if not provided by the user
    over_sampling_type = luigi.EnumParameter(enum=elmdpenum.OverSamplingTypes)

    def actual_task_code(self, df: pd.DataFrame):
        rseed = None
        over_sampler = None

        if self.random_seed != -1:
            rseed = self.random_seed

        if self.over_sampling_type is elmdpenum.OverSamplingTypes.RANDOM_OVER_SAMPLING:
            over_sampler = imbl_os.RandomOverSampler(random_state=rseed)
        elif self.over_sampling_type is elmdpenum.OverSamplingTypes.ADASYN:
            over_sampler = imbl_os.ADASYN(random_state=rseed)
        elif self.over_sampling_type is elmdpenum.OverSamplingTypes.SMOTE_REGULAR:
            over_sampler = imbl_os.SMOTE(random_state=rseed, kind='regular')
        elif self.over_sampling_type is elmdpenum.OverSamplingTypes.SMOTE_SVM:
            over_sampler = imbl_os.SMOTE(random_state=rseed, kind='svm')
        elif self.over_sampling_type is elmdpenum.OverSamplingTypes.SMOTE_BORDERLINE1:
            over_sampler = imbl_os.SMOTE(random_state=rseed, kind='borderline1')
        elif self.over_sampling_type is elmdpenum.OverSamplingTypes.SMOTE_BORDERLINE2:
            over_sampler = imbl_os.SMOTE(random_state=rseed, kind='borderline2')

        x, y = over_sampler.fit_sample(df.drop(self.label_column, axis=1), df[self.label_column])
        x[self.label_column] = y

        return x


class UnderSample(elmdptt.TaskOneToOne):
    label_column = luigi.Parameter()
    random_seed = luigi.IntParameter()  # Must be set to -1 if not provided by the user
    under_sampling_type = luigi.EnumParameter(enum=elmdpenum.OverSamplingTypes)

    def actual_task_code(self, df: pd.DataFrame):
        rseed = None
        under_sampler = None

        if self.random_seed != -1:
            rseed = self.random_seed

        if self.under_sampling_type is elmdpenum.UnderSamplingTypes.RANDOM_UNDER_SAMPLING:
            under_sampler = imbl_us.RandomUnderSampler(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.TOMEK_LINKS:
            under_sampler = imbl_us.TomekLinks(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.NEIGHBOURHOOD_CLEANING_RULE:
            under_sampler = imbl_us.NeighbourhoodCleaningRule(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.CONDENSED_NEAREST_NEIGHBOUR:
            under_sampler = imbl_us.CondensedNearestNeighbour(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.EDITED_NEAREST_NEIGHBOUR:
            under_sampler = imbl_us.EditedNearestNeighbours(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.REPEATED_EDITED_NEAREST_NEIGHBOUR:
            under_sampler = imbl_us.RepeatedEditedNearestNeighbours(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.ALL_KNN:
            under_sampler = imbl_us.AllKNN(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.CLUSTER_CENTROIDS_SOFT_VOTING:
            under_sampler = imbl_us.ClusterCentroids(random_state=rseed)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.CLUSTER_CENTROIDS_HARD_VOTING:
            under_sampler = imbl_us.ClusterCentroids(random_state=rseed, voting='hard')
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.NEARMISS_V1:
            under_sampler = imbl_us.NearMiss(random_state=rseed, version=1)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.NEARMISS_V2:
            under_sampler = imbl_us.NearMiss(random_state=rseed, version=2)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.NEARMISS_V3:
            under_sampler = imbl_us.NearMiss(random_state=rseed, version=3)
        elif self.under_sampling_type is elmdpenum.UnderSamplingTypes.ONE_SIDED_SELECTION:
            under_sampler = imbl_us.OneSidedSelection(random_state=rseed)

        x, y = under_sampler.fit_sample(df.drop(self.label_column, axis=1), df[self.label_column])
        x[self.label_column] = y

        return x


class LinearRegression(elmdptt.TaskModelInitialization):
    normalize_inputs = luigi.BoolParameter()

    def actual_task_code(self):
        model = linear_model.LinearRegression(normalize=self.normalize_inputs)
        return model


class LogisticRegressionClassifier(elmdptt.TaskModelInitialization):
    normalize_inputs = luigi.BoolParameter()
    random_seed = luigi.IntParameter()  # Must be set to -1 if not provided by the user
    attr_penalty = luigi.Parameter()  # Must be set to 'l2' if not provided by the user
    attr_c = luigi.FloatParameter()  # Must be set to 1.0 if not provided by the user

    def actual_task_code(self):
        rseed = None

        if self.random_seed != -1:
            rseed = self.random_seed

        model = linear_model.LogisticRegression(random_state=rseed, C=self.attr_c, penalty=self.attr_penalty)
        return model


class FitModel(elmdptt.TaskModelFitting):
    label_column = luigi.Parameter()

    def actual_task_code(self, model, df: pd.DataFrame):
        model.fit(df.drop(self.label_column, axis=1), df[self.label_column])
        return model


class RunModel(elmdptt.TaskModelRun):
    def actual_task_code(self, model, df: pd.DataFrame):
        predictions = model.predict(df.drop('satisfaction_level', axis=1))
        df['predictions'] = predictions
        return df


class KNN(elmdptt.TaskModelInitialization):
    n_neighbors = luigi.Parameter()

    def actual_task_code(self):
        model = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        return model


class DecisionTree(elmdptt.TaskModelInitialization):
    criterion = luigi.Parameter()
    max_depth = luigi.Parameter()
    min_samples_leaf = luigi.Parameter
    random_state = luigi.Parameter()
    max_leaf_nodes = luigi.Parameter()

    def actual_task_code(self):
        model = tree.DecisionTreeClassifier(criterion=self.criterion, max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf, random_state=self.random_state, max_leaf_nodes=self.max_leaf_nodes)
        return model


class RandomForest(elmdptt.TaskModelInitialization):
    n_estimators = luigi.Parameter()

    def actual_task_code(self):
        model = RandomForestClassifier(n_estimators=self.n_estimators)
        return model


class NeuralNetwork(elmdptt.TaskModelInitialization):
    solver = luigi.Parameter()
    hidden_layer_sizes = luigi.Parameter()
    random_state = luigi.Parameter()
    activation = luigi.Parameter()
    alpha = luigi.Parameter()
    learning_rate = luigi.Parameter()
    learning_rate_init = luigi.Parameter()
    max_iter = luigi.Parameter()

    def actual_task_code(self):
        model = MLPClassifier(solver=self.solver(), hidden_layer_sizes=self.hidden_layer_sizes,
                              random_state=self.random_state, activation=self.activation, alpha=self.alpha,
                              learning_rate=self.learning_rate, learning_rate_init=self.learning_rate_init,
                              max_iter=self.max_iter)
        return model


class KMeans(elmdptt.TaskModelInitialization):
    n_clusters = luigi.Parameter()
    init = luigi.Parameter()
    n_init = luigi.Parameter()
    max_iter = luigi.Parameter()
    tol = luigi.Parameter()

    def actual_task_code(self):
        model = KMeans(n_clusters=self.n_clusters, init=self.init, n_init=self.n_init, max_iter=self.max_iter, tol= self.tol)
        return model

