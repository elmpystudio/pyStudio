import sciluigi as sl
import pandas as pd
import pickle as pkl
import machine_learning_app.elmluigilib.elmdp_tasks_metadata as md
import json
import time

_paths_folder = '/home/admin/luigi_outputs/paths_output/'
_results_folder = '/home/admin/luigi_outputs/results_output/'
_models_folder = '/home/admin/luigi_outputs/models_output/'
_metadata_folder = '/home/admin/luigi_outputs/metadata_output/'
_sleep_duration = 0


def read_result(result_path):
    return pd.read_pickle(result_path)


def write_result(result_path, df):
    df.to_pickle(result_path)
    return result_path


def read_model(model_path):
    return pkl.load(open(model_path, 'rb'))


def write_model(model_path, model):
    pkl.dump(model, open(model_path, 'wb'))
    return model_path


def write_output_path(output_path, result_path):
    file = open(output_path, 'w')
    file.write(result_path)
    file.close()


def write_meta_data(md_path, task_md):
    with open(md_path, 'w') as outfile:
        json.dump(task_md.to_json(), outfile, ensure_ascii=False)


def generate_task_meta_data(self):
    return md.TaskMetaData(self.__class__.__name__, self.task_id)


def generate_data_output_meta_data(o_sequence, df):
    return md.TaskDataOutputMetaData(df.head(50), o_sequence, df.dtypes, len(df.index), df.describe())


class TaskNoneToOne(sl.Task):
    def actual_task_code(self):
        return None

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Actual Task Code
        result_first = self.actual_task_code()

        #  Write Meta Data
        task_md = generate_task_meta_data(self)
        task_md.add_output_meta_data(generate_data_output_meta_data(1, result_first))
        write_meta_data(_metadata_folder + self.task_id + '_task_meta_data.json', task_md)

        #  Task Data Output
        path1 = write_result(_results_folder + self.task_id + '_output_result_1.pkl', result_first)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)


class TaskModelInitialization(sl.Task):
    def actual_task_code(self):
        return None

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Actual Task Code
        model_first = self.actual_task_code()

        #  Task Model Output
        path1 = write_model(_models_folder + self.task_id + '_output_model_1.model', model_first)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)


class TaskModelFitting(sl.Task):
    def __init__(self, *args, **kwargs):
        super(sl.Task, self).__init__(*args, **kwargs)
        self.in_first = None
        self.in_second = None

    def actual_task_code(self, task_model_first, task_df_first):
        return task_model_first

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Task Input
        task_model_first = read_model(self.in_first().open().read())
        task_df_first = read_result(self.in_second().open().read())

        #  Actual Task Code
        model_first = self.actual_task_code(task_model_first, task_df_first)

        #  Task Model Output
        path1 = write_model(_models_folder + self.task_id + '_output_model_1.model', model_first)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)


class TaskModelRun(sl.Task):
    def __init__(self, *args, **kwargs):
        super(sl.Task, self).__init__(*args, **kwargs)
        self.in_first = None
        self.in_second = None

    def actual_task_code(self, task_model_first, task_df_first):
        return task_df_first

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Task Input
        task_model_first = read_model(self.in_first().open().read())
        task_df_first = read_result(self.in_second().open().read())

        #  Actual Task Code
        result_first = self.actual_task_code(task_model_first, task_df_first)

        #  Write Meta Data
        task_md = generate_task_meta_data(self)
        task_md.add_output_meta_data(generate_data_output_meta_data(1, result_first))
        write_meta_data(_metadata_folder + self.task_id + '_task_meta_data.json', task_md)

        #  Task Model Output
        path1 = write_result(_results_folder + self.task_id + '_output_result_1.pkl', result_first)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)


class TaskOneToOne(sl.Task):
    def __init__(self, *args, **kwargs):
        super(sl.Task, self).__init__(*args, **kwargs)
        self.in_first = None

    def actual_task_code(self, task_df_first):
        return task_df_first

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Task Input
        task_df_first = read_result(self.in_first().open().read())

        #  Actual Task Code
        result_first = self.actual_task_code(task_df_first)

        #  Write Meta Data
        task_md = generate_task_meta_data(self)
        task_md.add_output_meta_data(generate_data_output_meta_data(1, result_first))
        write_meta_data(_metadata_folder + self.task_id + '_task_meta_data.json', task_md)

        #  Task Data Output
        path1 = write_result(_results_folder + self.task_id + '_output_result_1.pkl', result_first)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)


class TaskTwoToOne(sl.Task):
    def __init__(self, *args, **kwargs):
        super(sl.Task, self).__init__(*args, **kwargs)
        self.in_first = None
        self.in_second = None

    def actual_task_code(self, task_df_first, task_df_second):
        return task_df_first

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Task Input
        task_df_first = read_result(self.in_first().open().read())
        task_df_second = read_result(self.in_second().open().read())

        #  Actual Task Code
        result_first = self.actual_task_code(task_df_first, task_df_second)

        #  Write Meta Data
        task_md = generate_task_meta_data(self)
        task_md.add_output_meta_data(generate_data_output_meta_data(1, result_first))
        write_meta_data(_metadata_folder + self.task_id + '_task_meta_data.json', task_md)

        #  Task Data Output
        path1 = write_result(_results_folder + self.task_id + '_output_result_1.pkl', result_first)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)


class TaskOneToTwo(sl.Task):
    def __init__(self, *args, **kwargs):
        super(sl.Task, self).__init__(*args, **kwargs)
        self.in_first = None

    def actual_task_code(self, task_df_first):
        return task_df_first, task_df_first

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def out_second(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_2.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Task Input
        task_df_first = read_result(self.in_first().open().read())

        #  Actual Task Code
        result_first, result_second = self.actual_task_code(task_df_first)

        #  Write Meta Data
        task_md = generate_task_meta_data(self)
        task_md.add_output_meta_data(generate_data_output_meta_data(1, result_first))
        task_md.add_output_meta_data(generate_data_output_meta_data(2, result_second))
        write_meta_data(_metadata_folder + self.task_id + '_task_meta_data.json', task_md)

        #  Task Data Output
        path1 = write_result(_results_folder + self.task_id + '_output_result_1.pkl', result_first)
        path2 = write_result(_results_folder + self.task_id + '_output_result_2.pkl', result_second)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)
        write_output_path(_paths_folder + self.task_id + '_output_path_2.txt', path2)


class TaskTwoToTwo(sl.Task):
    def __init__(self, *args, **kwargs):
        super(sl.Task, self).__init__(*args, **kwargs)
        self.in_first = None
        self.in_second = None

    def actual_task_code(self, task_df_first, task_df_second):
        return task_df_first, task_df_second

    def out_first(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_1.txt')

    def out_second(self):
        return sl.TargetInfo(self, _paths_folder + self.task_id + '_output_path_2.txt')

    def run(self):
        time.sleep(_sleep_duration)
        #  Task Input
        task_df_first = read_result(self.in_first().open().read())
        task_df_second = read_result(self.in_second().open().read())

        #  Actual Task Code
        result_first, result_second = self.actual_task_code(task_df_first, task_df_second)

        #  Write Meta Data
        task_md = generate_task_meta_data(self)
        task_md.add_output_meta_data(generate_data_output_meta_data(1, result_first))
        task_md.add_output_meta_data(generate_data_output_meta_data(2, result_second))
        write_meta_data(_metadata_folder + self.task_id + '_task_meta_data.json', task_md)

        #  Task Data Output
        path1 = write_result(_results_folder + self.task_id + '_output_result_1.pkl', result_first)
        path2 = write_result(_results_folder + self.task_id + '_output_result_2.pkl', result_second)

        #  Task Output Path
        write_output_path(_paths_folder + self.task_id + '_output_path_1.txt', path1)
        write_output_path(_paths_folder + self.task_id + '_output_path_2.txt', path2)


