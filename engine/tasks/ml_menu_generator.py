# this must be use in the future to generate frontEnd nodes(task/functions) menu in ML studio
from tasks.ml_menu import *

the_menu = Mlmenu([])

data_sources = MenuGroup(icon_name="fa fa-database", name="Data Sources")
data_manipulation = MenuGroup(icon_name="fa fa-wrench", name="Data Manipulation")
data_transformation = MenuGroup(icon_name="fa fa-refresh", name="Data Transformation")
data_sampling = MenuGroup(icon_name="fa fa-exchange", name="Data Sampling")
incremental_learning = MenuGroup(icon_name="fa fa-cogs", name="Incremental Learning")
machine_learning = MenuGroup(icon_name="fa fa-cogs", name="Machine Learning")
model_evaluation = MenuGroup(icon_name="fa fa-thumbs-up", name="Model Evaluation")

top = Group(icon_name="fa fa-cogs", name="top")
classic = Group(icon_name="fa fa-cogs", name="classic")
classification = Group(icon_name="fa fa-cogs", name="classification")
clustering = Group(icon_name="fa fa-cogs", name="clustering")
regression = Group(icon_name="fa fa-cogs", name="regression")


def make_the_menu():
    # global data_sources, data_manipulation, data_transformation, data_sampling, incremental_learning, \
    #     machine_learning, model_evaluation
    #
    # global top
    # global classic
    # global classification
    # global clustering
    # global regression

    machine_learning.groups.append(top)
    machine_learning.groups.append(classic)
    incremental_learning.groups.append(classification)
    incremental_learning.groups.append(clustering)
    incremental_learning.groups.append(regression)
    the_menu.groups.append(data_sources)
    the_menu.groups.append(data_manipulation)
    the_menu.groups.append(data_transformation)
    the_menu.groups.append(incremental_learning)
    the_menu.groups.append(machine_learning)
    the_menu.groups.append(model_evaluation)
    return the_menu


def add_in_place(n: Node):
    if n.kind == Kind.NO_INPUT:
        data_sources.nodes.append(n)
    elif n.kind == Kind.DATA_MANIPULATION:
        data_manipulation.nodes.append(n)
    elif n.kind == Kind.DATA_SAMPLING:
        data_sampling.nodes.append(n)
    elif n.kind == Kind.DATA_TRANSFORMATION:
        data_transformation.nodes.append(n)
    elif n.kind == Kind.INCREMENTAL_LEARNING:
        if n.kind == SubKind.CLASSIFICATION:
            classification.nodes.append(n)
        elif n.kind == SubKind.CLUSTERING:
            clustering.nodes.append(n)
        elif n.kind == SubKind.REGRESSION:
            regression.nodes.append(n)
    elif n.kind == Kind.MACHINE_LEARNING:
        if n.kind == SubKind.TOP:
            top.nodes.append(n)
        elif n.kind == SubKind.CLASSIC:
            classic.nodes.append(n)
    elif n.kind == Kind.MODEL_EVALUATION:
        model_evaluation.nodes.append(n)
    else:
        print('create your own!')


__model_type = dict(DecisionTreeClassifier="Classifier",
                    KNeighborsClassifier="Classifier",
                    Kmeans="Cluster",
                    LinearRegression="Regressor",
                    LogisticRegressionClassifier="Classifier",
                    MultilayerPerceptron_ClassifierClassifier="Classifier",
                    RandomForestClassifier="Classifier",
                    XGBRegressor="Regressor",
                    XGBClassifier="Classifier",
                    LGBMClassifier="Classifier",
                    LGBMRegressor="Regressor",
                    BaggingClassifier="Classifier",
                    CNNfinetune="Classifier",
                    CatBoost='Classifier',
                    Adaboost='Classifier',
                    RandomForestRegressor="Regressor",
                    LSTM_Model="Regressor",
                    MultinomialNB_Classifier='Classifier',
                    BernoulliNB_Classifier='Classifier',
                    Perceptron_Classifier='Classifier',
                    PassiveAggressive_Classifier='Classifier',
                    PassiveAggressive_Regressor='Regressor',
                    MiniBatchKMeans='Cluster',
                    SGDC_Calissifier='Classifier',
                    PreTrainedModel='Pretrained')

__nodes_grouping = dict(ReadCSV="Data Sources",
                        ApplySqlite="Data Manipulation",
                        ReplaceValue="Data Manipulation",
                        RowFilter="Data Manipulation",
                        DropMissing="Data Manipulation",
                        FillMissingWithMean="Data Manipulation",
                        FillMissingWithValue="Data Manipulation",
                        CategoryToDigits="Data Manipulation",
                        ChangeColumnsName="Data Manipulation",
                        ChangeDtypes="Data Manipulation",
                        ColumnBinning="Data Manipulation",
                        JoinData="Data Manipulation",
                        MeltingDf="Data Manipulation",
                        SelectColumns="Data Manipulation",
                        SplitData="Data Sampling",
                        UnderSample="Data Sampling",
                        OverSample="Data Sampling",
                        Normalized="Data Transformation",
                        Standardized="Data Transformation",
                        DecisionTree="Machine Learning",
                        KNeighborsClassifier="Machine Learning",
                        Kmeans="Machine Learning",
                        LinearRegression="Machine Learning",
                        LogisticRegressionClassifier="Machine Learning",
                        MultilayerPerceptron_ClassifierClassifier="Machine Learning",
                        RandomForestClassifier="Machine Learning",
                        RandomForestRegressor="Machine Learning",
                        XGBRegressor="Machine Learning",
                        XGBClassifier="Machine Learning",
                        LGBMClassifier="Machine Learning",
                        LGBMRegressor="Machine Learning",
                        BaggingClassifier="Machine Learning",
                        CNNfinetune="Machine Learning",
                        CatBoost='Machine Learning',
                        Adaboost='Machine Learning',
                        FitModel="Machine Learning",
                        RunModel="Machine Learning",
                        ClassificationMetrics="Model Evaluation",
                        ClusteringMetrics="Model Evaluation",
                        RegressionMetrics="Model Evaluation",
                        SelectDataset="Data Sources",
                        SplitTrainTest="Machine Learning",
                        LSTM_Model="Machine Learning",
                        PCA_PC="Data Manipulation",
                        ILV_PC="Data Manipulation",
                        MultinomialNB_Classifier='Machine Learning',
                        BernoulliNB_Classifier='Machine Learning',
                        Perceptron_Classifier='Machine Learning',
                        PassiveAggressive_Classifier='Machine Learning',
                        PassiveAggressive_Regressor='Machine Learning',
                        MiniBatchKMeans='Machine Learning',
                        SGDC_Calissifier='Machine Learning',
                        PreTrainedModel='Pre trained model')
__nodes_display_names = dict(ReadCSV="Read CSV",
                             ApplySqlite="Apply SQL",
                             ReplaceValue="Replace Value",
                             RowFilter="Row Filter",
                             DropMissing="Drop Missing",
                             FillMissingWithMean="Fill Missing with Mean",
                             FillMissingWithValue="Fill Missing with Value",
                             CategoryToDigits="Categorical to Numeric",
                             ChangeColumnsName="Change Column Name",
                             ChangeDtypes="Change Data Type",
                             ColumnBinning="Column Binning",
                             JoinData="Join Data",
                             MeltingDf="Column Melting",
                             SelectColumns="Column Selector",
                             SplitData="Data Splitter",
                             UnderSample="Under Sampling",
                             OverSample="Over Sampling",
                             Normalized="Normalizer",
                             Standardized="Standardizer",
                             DecisionTree="Decision Tree",
                             KNeighborsClassifier="k-Nearest Neighbor",
                             Kmeans="k-Means",
                             LinearRegression="Linear Regression",
                             LogisticRegressionClassifier="Logistic Regression Classifier",
                             MultilayerPerceptron_ClassifierClassifier="MultilayerPerceptron_ClassifierClassifier",
                             XGBRegressor="XGBRegressor",
                             XGBClassifier="XGBClassifier",
                             LGBMClassifier="LGBMClassifier",
                             LGBMRegressor="LGBMRegressor",
                             BaggingClassifier='BaggingClassifier',
                             CNNfinetune='CNNfinetune',
                             CatBoost='CatBoost',
                             Adaboost='Adaboost',
                             RandomForestClassifier="Random Forest Classifier",
                             RandomForestRegressor="Random Forest Regression",
                             FitModel="Fit Model",
                             RunModel="Run Model",
                             ClassificationMetrics="Classification Evaluator",
                             ClusteringMetrics="Clustering Evaluator",
                             RegressionMetrics="Regression Evaluator",
                             SelectDataset="Select Dataset",
                             SplitTrainTest="STTE",
                             LSTM_Model="LSTM_Model",
                             PCA_PC="PCA",
                             ILV_PC="Ignore Low Variance",
                             MultinomialNB_Classifier='MultinomialNB_Classifier Classifier',
                             BernoulliNB_Classifier='BernoulliNB_Classifier Classifier',
                             Perceptron_Classifier='Perceptron_Classifier Classifier',
                             PassiveAggressive_Classifier='Passive Aggressive Classifier',
                             PassiveAggressive_Regressor='Passive Aggressive Regressor',
                             MiniBatchKMeans='Mini Batch KMeans',
                             SGDC_Calissifier='SGDC_Calissifier',
                             PreTrainedModel='PreTrainedModel')

__parameters_names = {
    'ColumnBinning': {
        'no_bins': 'Number of Bins',
        'col_name': 'Column Name'
    },
    'ReadCSV': {
        'csv_path': 'CSV Path'
    },
    'SelectDataset': {
        'dataset_name': 'Dataset Name'
    },
    'ClusteringMetrics': {
        'predict_column': 'Predicted Column',
        'label_column': 'Label Column'
    },
    'LogisticRegressionClassifier': {
        'normalize_inputs': 'Normalize Inputs',
        'attr_c': 'C Value',
        'random_seed': 'Random Seed',
        'attr_penalty': 'Penalty'
    },
    'FillMissingWithMean': {
        'col_names': 'Column Name(s)'
    },
    'RegressionMetrics': {
        'predict_column': 'Predicted Column',
        'label_column': 'Label Column'
    },
    'JoinData': {
        'left_col_names': 'Left Columns',
        'right_col_names': 'Right Columns',
        'join_type': 'Join Type'
    },
    'UnderSample': {
        'under_sampling_type': 'Under Sampling Type',
        'label_column': 'Label Column',
        'random_seed': 'Random Seed'
    },
    'Kmeans': {
        'max_iter': 'Max Number of Iterations',
        'tol': 'Tolerance',
        'init': 'Initialization Method',
        'n_init': 'Initialization Number',
        'n_clusters': 'Number of Clusters'
    },
    'FitModel': {
        'label_column': 'Label Column'
    },
    'ChangeDtypes': {
        'changed_columns': 'Changed Column(s)'
    },
    'SelectColumns': {
        'col_names': 'Column Name(s)'
    },
    'KNeighborsClassifier': {
        'n_neighbors': 'Number of Neighbors'
    },
    'ApplySqlite': {
        'sqlite_query': 'SQLite Query'
    },
    'LinearRegression': {
        'normalize': 'Normalize Inputs'
    },
    'RandomForestClassifier': {
        'n_estimators': 'Number of Estimators'
    },
    'XGBRegressor': {
        'tree_method': 'Tree Method'
    },
    'XGBClassifier': {
        'booster': 'Booster'
    },
    'LGBMClassifier': {
        'random_state': 'A number to represent random state'
    },
    'CNNfinetune': {
        'num_classes': 'A number of clases'
    },
    'BaggingClassifier': {
        'n_estimators': 'A number or estimators',
        'max_features': 'the mx features'
    },
    'LGBMRegressor': {
        'num_leaves': 'Number of leaves',
        'learning_rate': 'Learning rate in 0.... way',
        'n_estimators': 'number of estimators'
    },
    'CatBoost': {
        'iterations': 'Iterations number',
        'task_type': 'Use GPU if you can'
    },
    'Adaboost': {
        'algorithm': 'The algorithm'
    },
    'RandomForestRegressor': {
        'n_estimators': 'Number of Estimators',
        'criterion': 'Criterion',
        'min_samples_split': 'Minimum Samples to Split',
        'min_samples_leaf': 'Minimum Samples in a Leaf',
        'random_state': 'Random Seed'
    },
    'ChangeColumnsName': {
        'col_name_dict': 'Column Name(s)'
    },
    'RowFilter': {
        'filter_expression': 'Filter Expression'
    },
    'OverSample': {
        'label_column': 'Label Column',
        'random_seed': 'Random Seed',
        'over_sampling_type': 'Over Sampling Type'
    },
    'ReplaceValue': {
        'value_to_replace': 'Value to Replace',
        'col_names': 'Column Name(s)',
        'replacement_value': 'Replacement Value'
    },
    'DecisionTree': {
        'criterion': 'Criterion',
        'min_samples_split': 'Minimum Samples to Split',
        'min_samples_leaf': 'Minimum Samples in a Leaf',
        'max_depth': 'Maximum Depth',
        'max_leaf_nodes': 'Max Leaf Nodes',
        'random_state': 'Random Seed'
    },
    'CategoryToDigits': {
        'col_names': 'Column Name(s)'
    },
    'MeltingDf': {
        'value_vars': 'Value Variables',
        'id_vars': 'Identifier Variables'
    },
    'MultilayerPerceptron_ClassifierClassifier': {
        'max_iter': 'Max Number of Iterations',
        'solver': 'Solver',
        'learning_rate': 'Learning Rate',
        'random_state': 'Random Seed',
        'activation': 'Activation',
        'alpha': 'Alpha',
        'hidden_layer_sizes': 'Hidden Layer Size',
        'learning_rate_init': 'Learning'
    },
    'ClassificationMetrics': {
        'predict_column': 'Predicted Column',
        'label_column': 'Label Column'
    },
    'SplitData': {
        'partition_percentage': 'Partition Percentage'
    },
    'RunModel': {
        'label_column': 'Label Column'
    },
    'Normalized': {
        'col_names': 'Column Name(s)'
    },
    'FillMissingWithValue': {
        'col_names': 'Column Name(s)',
        'replacement_value': 'Replacement Value'
    },
    'Standardized': {
        'col_names': 'Column Name(s)'
    },
    'DropMissing': {
        'drop_type': 'Drop Type'
    },
    'SplitTrainTest': {
        'label_column': 'Label Column',
        'partition_percentage': 'Partition Percentage'
    },
    'LSTM_Model': {
        'epochs': 'Number Of Epochs'
    },
    'SGDC_Calissifier': {
        'learning_rate': 'Learning rate'
    },
    'PreTrainedModel': {
        'model_name': 'Model name'
    },
    'PCA_PC': {
        'label_column': 'Label Column',
        'pca_components': 'Number of PCA Components'
    },
    'ILV_PC': {
        'label_column': 'Label Column'
    },
    'MultinomialNB_Classifier': {
        'alpha': 'alpha',
        'fit_prior': 'Fit Prior'
    },
    'BernoulliNB_Classifier': {
        'alpha': 'alpha',
        'fit_prior': 'Fit Prior'
    },
    'Perceptron_Classifier': {
        'penalty': 'Penalty',
        'alpha': 'Alpha',
        'fit_intercept': 'Fit Intercept'
    },
    'PassiveAggressive_Classifier': {
        'step_size': 'Step Size',
        'fit_intercept': 'Fit Intercept'
    },
    'PassiveAggressive_Regressor': {
        'step_size': 'Step Size',
        'fit_intercept': 'Fit Intercept',
        'epsilon': 'Epsilon'
    },
    'MiniBatchKMeans': {
        'n_clusters': 'Number of clusters',
        'num_iter': 'Number of iterations'
    }
}

__parameters_default_values = {
    'ColumnBinning': {
        'no_bins': '5',
        'col_name': ''
    },
    'ReadCSV': {
        'csv_path': ''
    },
    'SelectDataset': {
        'dataset_name': ''
    },
    'ClusteringMetrics': {
        'predict_column': '',
        'label_column': ''
    },
    'LogisticRegressionClassifier': {
        'fit_intercept': '',
        'C': '1',
        'penalty': 'l2'
    },
    'FillMissingWithMean': {
        'col_names': ''
    },
    'RegressionMetrics': {
        'predict_column': '',
        'label_column': ''
    },
    'JoinData': {
        'left_col_names': '',
        'right_col_names': '',
        'join_type': 'INNER_JOIN'
    },
    'UnderSample': {
        'under_sampling_type': '',
        'label_column': '',
        'random_seed': '0'
    },
    'Kmeans': {
        'max_iter': '',
        'tol': '',
        'init': '',
        'n_init': '',
        'n_clusters': ''
    },
    'FitModel': {
        'label_column': ''
    },
    'ChangeDtypes': {
        'changed_columns': ''
    },
    'SelectColumns': {
        'col_names': ''
    },
    'KNeighborsClassifier': {
        'n_neighbors': ''
    },
    'ApplySqlite': {
        'sqlite_query': ''
    },
    'LinearRegression': {
        'normalize': 'True'
    },
    'RandomForestClassifier': {
        'n_estimators': '10'
    },
    'XGBRegressor': {
        'tree_method': 'hist'
    },
    'XGBClassifier': {
        'booster': 'gbtree'
    },
    'LGBMClassifier': {
        'random_state': 42
    },
    'LGBMRegressor': {
        'num_leaves': '31',
        'learning_rate': '0.05',
        'n_estimators': '20'
    },
    'CNNfinetune': {
        'num_classes': '10'
    },
    'BaggingClassifier': {
        'n_estimators': '10',
        'max_features': '1.0'
    },
    'CatBoost': {
        'iterations': 100,
        'task_type': 'GPU'
    },
    'Adaboost': {
        'algorithm': 'SAMME.R'
    },
    'RandomForestRegressor': {
        'n_estimators': '10',
        'criterion': 'mse',
        'min_samples_split': '6',
        'min_samples_leaf': '3',
        'random_state': '0'
    },
    'ChangeColumnsName': {
        'col_name_dict': ''
    },
    'RowFilter': {
        'filter_expression': ''
    },
    'OverSample': {
        'label_column': '',
        'random_seed': '0',
        'over_sampling_type': ''
    },
    'ReplaceValue': {
        'value_to_replace': '',
        'col_names': '',
        'replacement_value': ''
    },
    'DecisionTreeClassifier': {
        'criterion': 'gini',
        'min_samples_split': '6',
        'min_samples_leaf': '3',
        'max_depth': '',
        'max_leaf_nodes': '',
        'random_state': '0'
    },
    'CategoryToDigits': {
        'col_names': ''
    },
    'MeltingDf': {
        'value_vars': '',
        'id_vars': ''
    },
    'MultilayerPerceptron_ClassifierClassifier': {
        'max_iter': '',
        'solver': '',
        'learning_rate': '',
        'random_state': '0',
        'activation': '',
        'alpha': '',
        'hidden_layer_sizes': '',
        'learning_rate_init': ''
    },
    'ClassificationMetrics': {
        'predict_column': '',
        'label_column': ''
    },
    'SplitData': {
        'partition_percentage': ''
    },
    'RunModel': {
        'label_column': ''
    },
    'Normalized': {
        'col_names': ''
    },
    'FillMissingWithValue': {
        'col_names': '',
        'replacement_value': ''
    },
    'Standardized': {
        'col_names': ''
    },
    'DropMissing': {
        'drop_type': ''
    },
    'SplitTrainTest': {
        'label_column': '',
        'partition_percentage': ''
    },
    'LSTM_Model': {
        'epochs': '100'
    },
    'SGDC_Calissifier': {
        'learning_rate': 'optimal'
    },
    'PreTrainedModel': {
        'model_name': ''
    },
    'PCA_PC': {
        'label_column': '',
        'pca_components': ''
    },
    'ILV_PC': {
        'label_column': ''
    },
    'MultinomialNB_Classifier': {
        'alpha': '1.0',
        'fit_prior': 'True'
    },
    'BernoulliNB_Classifier': {
        'alpha': '1.0',
        'fit_prior': 'True'
    },
    'Perceptron_Classifier': {
        'penalty': 'None',
        'alpha': '0.0001',
        'fit_intercept': 'True'
    },
    'PassiveAggressive_Classifier': {
        'step_size': '1.0',
        'fit_intercept': 'True'
    },
    'PassiveAggressive_Regressor': {
        'step_size': '1.0',
        'fit_intercept': 'True',
        'epsilon': '0.1'
    },
    'MiniBatchKMeans': {
        'n_clusters': '8',
        'num_iter': '100'
    }

}

__parameters_types = {
    'ColumnBinning': {
        'no_bins': '',
        'col_name': 'single_column'
    },
    'ReadCSV': {
        'csv_path': ''
    },
    'SelectDataset': {
        'dataset_name': ''
    },
    'ClusteringMetrics': {
        'predict_column': 'single_column',
        'label_column': 'single_column'
    },
    'LogisticRegressionClassifier': {
        'fit_intercept': '',
        'C': '1',
        'penalty': ''
    },
    'FillMissingWithMean': {
        'col_names': 'multiple_columns'
    },
    'RegressionMetrics': {
        'predict_column': 'single_column',
        'label_column': 'single_column'
    },
    'JoinData': {
        'left_col_names': 'multiple_columns',
        'right_col_names': 'multiple_columns',
        'join_type': ''
    },
    'UnderSample': {
        'under_sampling_type': '',
        'label_column': 'single_column',
        'random_seed': ''
    },
    'Kmeans': {
        'max_iter': '',
        'tol': '',
        'init': '',
        'n_init': '',
        'n_clusters': ''
    },
    'FitModel': {
        'label_column': 'single_column'
    },
    'ChangeDtypes': {
        'changed_columns': 'columns_with_types'
    },
    'SelectColumns': {
        'col_names': 'multiple_columns'
    },
    'KNeighborsClassifier': {
        'n_neighbors': ''
    },
    'ApplySqlite': {
        'sqlite_query': 'text_area'
    },
    'LinearRegression': {
        'normalize': ''
    },
    'RandomForestClassifier': {
        'n_estimators': ''
    },
    'XGBRegressor': {
        'tree_method': ''
    },
    'XGBClassifier': {
        'booster': ''
    },
    'LGBMClassifier': {
        'random_state': ''
    },
    'LGBMRegressor': {
        'num_leaves': '',
        'learning_rate': '',
        'n_estimators': ''
    },
    'CNNfinetune': {
        'num_classes': ''
    },
    'BaggingClassifier': {
        'n_estimators': '',
        'max_features': ''
    },
    'CatBoost': {
        'iterations': '',
        'task_type': ''
    },
    'Adaboost': {
        'algorithm': ''
    },
    'RandomForestRegressor': {
        'n_estimators': '',
        'criterion': '',
        'min_samples_split': '',
        'min_samples_leaf': '',
        'random_state': ''
    },
    'ChangeColumnsName': {
        'col_name_dict': 'columns_with_names'
    },
    'RowFilter': {
        'filter_expression': 'text_area'
    },
    'OverSample': {
        'label_column': 'single_column',
        'random_seed': '',
        'over_sampling_type': ''
    },
    'ReplaceValue': {
        'value_to_replace': '',
        'col_names': 'multiple_columns',
        'replacement_value': ''
    },
    'DecisionTree': {
        'criterion': '',
        'min_samples_split': '',
        'min_samples_leaf': '',
        'max_depth': '',
        'max_leaf_nodes': '',
        'random_state': ''
    },
    'CategoryToDigits': {
        'col_names': 'multiple_columns'
    },
    'MeltingDf': {
        'value_vars': '',
        'id_vars': ''
    },
    'MultilayerPerceptron_ClassifierClassifier': {
        'max_iter': '',
        'solver': '',
        'learning_rate': '',
        'random_state': '',
        'activation': '',
        'alpha': '',
        'hidden_layer_sizes': '',
        'learning_rate_init': ''
    },
    'ClassificationMetrics': {
        'predict_column': 'single_column',
        'label_column': 'single_column'
    },
    'SplitData': {
        'partition_percentage': ''
    },
    'RunModel': {
        'label_column': 'single_column'
    },
    'Normalized': {
        'col_names': 'multiple_columns'
    },
    'FillMissingWithValue': {
        'col_names': 'multiple_columns',
        'replacement_value': ''
    },
    'Standardized': {
        'col_names': 'multiple_columns'
    },
    'DropMissing': {
        'drop_type': ''
    },
    'SplitTrainTest': {
        'label_column': 'single_column',
        'partition_percentage': 'Partition Percentage'
    },
    'LSTM_Model': {
        'epochs': ''
    },
    'SGDC_Calissifier': {
        'learning_rate': ''
    },
    'PreTrainedModel': {
        'model_name': ''
    },
    'PCA_PC': {
        'label_column': 'single_column',
        'pca_components': ''
    },
    'ILV_PC': {
        'label_column': 'single_column'
    },
    'MultinomialNB_Classifier': {
        'alpha': '',
        'fit_prior': ''
    },
    'BernoulliNB_Classifier': {
        'alpha': '',
        'fit_prior': ''
    },
    'Perceptron_Classifier': {
        'penalty': '',
        'alpha': '',
        'fit_intercept': ''
    },
    'PassiveAggressive_Classifier': {
        'step_size': '',
        'fit_intercept': ''
    },
    'PassiveAggressive_Regressor': {
        'step_size': '',
        'fit_intercept': '',
        'epsilon': ''
    },
    'MiniBatchKMeans': {
        'n_clusters': '',
        'num_iter': ''
    }
}


def get_nodes_grouping():
    return __nodes_grouping


def get_nodes_display_names():
    return __nodes_display_names


def get_parameters_names():
    return __parameters_names


def get_parameters_default_values():
    return __parameters_default_values


def get_parameters_types():
    return __parameters_types


def get_task_params(task_name):
    return __parameters_default_values[task_name]


def get_model_type(model_name):
    return __model_type[model_name]
