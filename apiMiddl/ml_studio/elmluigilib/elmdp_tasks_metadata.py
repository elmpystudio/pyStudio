import machine_learning_app.elmluigilib.elmdp_enumerations as elmdpenum
import json


class TaskOutputMetaData:
    def __init__(self, output_sequence, output_type: elmdpenum.TaskOutputMetaDataTypes):
        self.output_sequence = output_sequence
        self.output_type = output_type

    def to_dict(self):
        return {'output_sequence': self.output_sequence, 'output_type': self.output_type}


class TaskDataOutputMetaData(TaskOutputMetaData):
    def __init__(self, sample_df, o_sequence, dtypes, number_of_records, df_description):
        super(TaskDataOutputMetaData, self).__init__(o_sequence, elmdpenum.TaskOutputMetaDataTypes.DATA_OUTPUT.value)
        self.sample_df = sample_df
        self.dtypes = dtypes
        self.number_of_records = number_of_records
        self.df_description = df_description

    def to_dict(self):
        meta_data = super(TaskDataOutputMetaData, self).to_dict()
        meta_data['number_of_records'] = self.number_of_records
        meta_data['dtypes'] = self._dtypes_to_dict_parser(self.dtypes)
        meta_data['df_description'] = self.df_description.to_dict()
        meta_data['sample_data'] = self.sample_df.to_dict(orient='records')
        return meta_data

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def _dtypes_to_dict_parser(dtypes):
        col_names = dtypes.keys().values.tolist()
        col_dtypes = [str(col).replace('dtype(\'', '').replace('\')', '') for col in dtypes.values.tolist()]
        return dict(zip(col_names, col_dtypes))


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
        return json.dumps(self.to_dict())