import requests
import json
from django.conf import settings

ML_ROOT_URL = settings.ML_ROOT_URL
MAIN_PATH = ''


# TODO refactor for sake of shame...

class Service:

    def execute_workflow(self, workflow_json):
        url = ML_ROOT_URL + 'start_workflow'
        r = requests.post(url=url, json=workflow_json)
        print("execute_workflow ", r.text)
        return r.text

    def get_workflow_progress(self, workflow_id):
        url = ML_ROOT_URL + MAIN_PATH + 'status/' + workflow_id
        print("get_workflow_progress url: ", url)
        r = requests.get(url)
        print("get_workflow_progress ", r.text)
        return r.text

    def get_node_output_details(self, node_details_json):
        url = ML_ROOT_URL + 'get_node_output'
        node_output = requests.post(url=url, json=node_details_json)
        return node_output.text

    def deploy_workflow(self, workflow_json):
        url = ML_ROOT_URL + 'deploy_workflow'
        response = requests.post(url=url, json=workflow_json)
        return response.text

    def get_evaluation_metrics(self, json_request):
        url = ML_ROOT_URL + MAIN_PATH + 'get_eval_metrics'
        node_output = requests.post(url=url, json=json_request)
        return node_output.text

    def get_roc_chart(self, json_request):
        url = ML_ROOT_URL + 'get_roc_chart'
        roc_image = requests.post(url=url, json=json_request)
        return roc_image.text

    def get_output_histogram(self, json_request):
        url = ML_ROOT_URL + 'get_node_output_hist'
        json_response = requests.post(url=url, json=json_request)
        return json_response.text

    def get_output_corr_matrix(self, json_request):
        url = ML_ROOT_URL + 'get_node_output_corr_matrix'
        json_response = requests.post(url=url, json=json_request)
        return json_response.text

    def get_output_pairwise(self, json_request):
        url = ML_ROOT_URL + MAIN_PATH + 'get_node_output_pairwise'
        json_response = requests.post(url=url, json=json_request)
        return json_response.text

    def get_node_metadata(self, json_request):
        url = ML_ROOT_URL + MAIN_PATH + 'get_workflow_ports_md'
        json_response = requests.post(url=url, json=json_request)
        return json_response

    def get_model_info(self, json_request):
        url = ML_ROOT_URL + MAIN_PATH + 'get_model_info'
        json_response = requests.post(url=url, json=json_request)
        return json_response

    # def start_deployed_workflow(self, json_request):
    #     url = ML_ROOT_URL + MAIN_PATH + 'start_deployed_workflow'
    #     json_response = requests.post(url=url, json=json_request)
    #     return json_response
