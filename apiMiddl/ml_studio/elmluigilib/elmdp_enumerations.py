from enum import Enum


# Enums
class DropMissingTypes(Enum):
    DROP_ROW_WITH_MISSING = 0
    DROP_EMPTY_ROW = 1
    DROP_EMPTY_COLUMN = 2


class JoinDataTypes(Enum):
    INNER_JOIN = 'inner'
    LEFT_JOIN = 'left'
    RIGHT_JOIN = 'right'
    OUTER_JOIN = 'outer'


class OverSamplingTypes(Enum):
    RANDOM_OVER_SAMPLING = 'randomOverSampling'
    ADASYN = 'adasyn'
    SMOTE_REGULAR = 'regular'
    SMOTE_BORDERLINE1 = 'borderline1'
    SMOTE_BORDERLINE2 = 'borderline2'
    SMOTE_SVM = 'svm'


class UnderSamplingTypes(Enum):
    TOMEK_LINKS = 'tomek_links'
    ONE_SIDED_SELECTION = 'one_sided_selection'
    RANDOM_UNDER_SAMPLING = 'random_under_sampling'
    NEIGHBOURHOOD_CLEANING_RULE = 'ncr'
    CONDENSED_NEAREST_NEIGHBOUR = 'condensed_nn'
    NEARMISS_V1 = 'nearmiss1'
    NEARMISS_V2 = 'nearmiss2'
    NEARMISS_V3 = 'nearmiss3'
    CLUSTER_CENTROIDS_SOFT_VOTING = 'ccsv'
    CLUSTER_CENTROIDS_HARD_VOTING = 'cchv'
    EDITED_NEAREST_NEIGHBOUR = 'enn'
    REPEATED_EDITED_NEAREST_NEIGHBOUR = 'renn'
    ALL_KNN = 'all_knn'


class TaskOutputMetaDataTypes(Enum):
    DATA_OUTPUT = 'data_output'
    MODEL_OUTPUT = 'model_output'
