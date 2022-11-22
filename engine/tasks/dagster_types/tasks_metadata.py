import tasks.dagster_types.enums as elmdpenum
import json


class TaskOutputMetaData:
    def __init__(self, output_sequence, output_label, output_type: elmdpenum.TaskOutputMetaDataTypes):
        self.output_sequence = output_sequence
        self.output_label = output_label
        self.output_type = output_type

    def to_dict(self):
        return {'output_sequence': self.output_sequence, 'output_label': self.output_label, 'output_type': self.output_type}


class TaskModelOutputMetaData(TaskOutputMetaData):
    def __init__(self, o_sequence, o_label, model_md):
        super(TaskModelOutputMetaData, self).__init__(o_sequence, o_label, elmdpenum.TaskOutputMetaDataTypes.MODEL_OUTPUT.value)
        self.model_md = model_md

    def to_dict(self):
        meta_data = super(TaskModelOutputMetaData, self).to_dict()
        meta_data.update(self.model_md)
        return meta_data

    def to_json(self):
        return json.dumps(self.to_dict())


class TaskDataOutputMetaData(TaskOutputMetaData):
    def __init__(self, sample_df, o_sequence, o_label, dtypes, number_of_records, df_description, df_info, explanation=''):
        super(TaskDataOutputMetaData, self).__init__(o_sequence, o_label, elmdpenum.TaskOutputMetaDataTypes.DATA_OUTPUT.value)
        self.sample_df = sample_df
        self.explanation = explanation
        self.dtypes = dtypes
        self.number_of_records = number_of_records
        self.df_description = df_description
        self.df_info = df_info

    def to_dict(self):
        meta_data = super(TaskDataOutputMetaData, self).to_dict()
        meta_data['number_of_records'] = self.number_of_records
        meta_data['dtypes'] = self._dtypes_to_dict_parser(self.dtypes)
        meta_data['dtypes_list'] = self._dtypes_to_list_parser(self.dtypes)
        meta_data['df_description'] = self.df_description.to_dict()
        meta_data['sample_data'] = self.sample_df.to_dict(orient='records')
        meta_data['df_info'] = self.df_info
        meta_data['explanation'] = self.explanation
        return meta_data

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def _dtypes_to_dict_parser(dtypes):
        col_names = list(dtypes.keys())
        col_dtypes = [col for col in list(dtypes.values())]
        return dict(zip(col_names, col_dtypes))

    @staticmethod
    def _dtypes_to_list_parser(dtypes):
        col_names = list(dtypes.keys())
        col_dtypes = [col for col in list(dtypes.values())]
        dtypes_list = []
        for n, t in zip(col_names, col_dtypes):
            dtypes_list.append(dict(col_name=n, col_dtype=t))
        return dtypes_list


class TaskMetaData:
    def __init__(self, task_name, task_id):
        self.task_name = task_name
        self.task_id = task_id
        self.outputs_list = []
        self.number_of_outputs = 0

    def add_output_meta_data(self, output_meta_data):
        self.outputs_list.append(output_meta_data)
        self.number_of_outputs += 1

    def to_dict(self):
        meta_data = {'task_name': self.task_name, 'task_id': self.task_id}
        outputs_dict = []

        for output in self.outputs_list:
            outputs_dict.append(output.to_dict())

        if len(outputs_dict) > 0:
            meta_data['outputs'] = outputs_dict

        return meta_data

    def to_json(self):
        return json.dumps(str(self.to_dict()))