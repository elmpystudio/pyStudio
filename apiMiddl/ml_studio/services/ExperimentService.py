#from ml_studio.dao import DatasetDao
#from ..dao import ExperimentDao
from ml_studio.models import *
from datetime import datetime as dt
import json

class ExperimentService:

    def get_experiments_by_userId(userId_json):
        userId = userId_json['userId']
        mls = MlWorkflow.objects.filter(user=userId)
        #mls = MlWorkflow.objefilter(user=userId_json)

        return mls

    def create_experiment(json_str):
        #print(json_str)
        #print(type(json_str))
        #mls = MlWorkflow.objects.filter(user=userId)
        print("---------CREATE-------------")
        print(json_str)
        print("----------------------")
        return MlWorkflow.objects.create(user_id=json_str['experimentId'], title=json_str['experimentName'],
                                         wf_json=json.dumps(json_str['workflowJson']), creation_ts=dt.now())
        #return connection.execute(sql.update(table).where(table.columns.id == int(json_str['experimentId'])).values(
        #wf_json=json.dumps(json_str['workflowJson'])), last_save=time)

    def save_workflow_json(experiment_json):
        print("---------SAVE-------------")
        print(experiment_json)
        print("----------------------")
        exp = MlWorkflow.objects.filter(id=experiment_json['experimentId'])[0]
        exp.wf_json = json.dumps(experiment_json['workflowJson'])
        exp.last_save = dt.now()
        return exp.save()

    def get_workflow_by_experimentId(experiment_json):
        return ExperimentDao.get_workflow_json(experiment_json)

    def save_deployed_workflow(workflow_json):
        return ExperimentDao.save_deployed_workflow(workflow_json)

    def get_datasets_by_user_id(user_id):
        return DatasetDao.list_datasets_by_user_id(user_id)

    def get_dataset_by_uuid(self, dataset_uuid):
        return DatasetDao.get_dataset_by_uuid(dataset_uuid)
