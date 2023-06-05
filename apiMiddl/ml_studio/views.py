import os
import uuid
import io
import pandas as pd
# import pandas_profiling as pprof
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .services import service as service
from .services.ExperimentService import ExperimentService as experiment_service
from timeit import default_timer as timer
import json
import requests
from django.http import JsonResponse
from django.conf import settings
import kaggle

@login_required(login_url=reverse_lazy('accounts:login'), redirect_field_name=None)
def index(request):
    current_user_id = request.user.id
    context = {
        'current_user_id': current_user_id,
    }
    return render(request, "machine_learning/experiments.html", context)

@csrf_exempt
def get_nodes_list(request):
    node_list = open("ml_studio/static/node_list.json").read()
    return HttpResponse(node_list, content_type="application/json")


@csrf_exempt
def execute_workflow(request):
    workflow_json = json.loads(request.body.decode('utf-8'))
    #print('workflow formatted: ', workflow_json)
    return HttpResponse(service.Service().execute_workflow(workflow_json), content_type="application/json")


@csrf_exempt
def get_workflow_progress(request, workflow_id):
    workflow_progress_json = service.Service.get_workflow_progress(request, workflow_id)
    return HttpResponse(workflow_progress_json, content_type="application/json")


@csrf_exempt
def get_node_output(request):
    workflow_json = json.loads(request.body.decode('utf-8'))
    workflow_progress_json = service.Service.get_node_output_details(request, workflow_json)
    return HttpResponse(workflow_progress_json, content_type="application/json")

@csrf_exempt
def get_eval_metrics(request):
    workflow_json = json.loads(request.body.decode('utf-8'))
    json_response = service.Service.get_evaluation_metrics(request, workflow_json)
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def get_roc_chart(request):
    json_str = json.loads(request.body.decode('utf-8'))
    json_response = service.Service.get_roc_chart(request, json_str)
    return HttpResponse(json_response, content_type="application/text")

@csrf_exempt
def get_model_info(request):
    json_str = json.loads(request.body.decode('utf-8'))
    json_response = service.Service.get_model_info(request, json_str)
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def get_node_metadata(request):
    json_str = json.loads(request.body.decode('utf-8'))
    json_response = service.Service.get_node_metadata(request, json_str)
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def get_output_histogram(request):
    json_str = json.loads(request.body.decode('utf-8'))
    json_response = service.Service.get_output_histogram(request, json_str)
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def get_output_pairwise(request):
    json_str = json.loads(request.body.decode('utf-8'))
    #json_str = ""
    json_response = service.Service.get_output_pairwise(request, json_str)
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def get_output_corr_matrix(request):
    json_str = json.loads(request.body.decode('utf-8'))
    json_response = service.Service.get_output_corr_matrix(request, json_str)
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def create_experiment(request):
    json_str = json.loads(request.body.decode('utf-8'))
    response = experiment_service.create_experiment(json_str)
    return HttpResponse(response, content_type="application/json")

@csrf_exempt
def get_experiments_by_userId(request):
    #print("-----------------------------------------")
    #print(request.body.decode('utf-8'))
    #print("-----------------------------------------")
    json_str = json.loads(request.body.decode('utf-8'))
    response = experiment_service.get_experiments_by_userId(json_str)
    return HttpResponse(response, content_type="application/json")

@csrf_exempt
def save_workflow(request):
    json_str = json.loads(request.body.decode('utf-8'))
    response = experiment_service.save_workflow_json(json_str)
    return HttpResponse(response, content_type="application/json")

@csrf_exempt
def retrieve_workflow_by_experimentId(request):
    if len(request.body) == 0:
        return HttpResponse("Nothing", content_type="application/json")

    json_str = json.loads(request.body.decode('utf-8'))
    response = experiment_service.get_workflow_by_experimentId(json_str)
    #print(response)
    return HttpResponse(response, content_type="application/json")


@csrf_exempt
def deploy_workflow(request):

    json_str = json.loads(request.body.decode('utf-8'))

    userId = json_str['userId']
    experimentName = jsKAGGLE_DATASETSon_str['experimentName']
    wf_unique_id = json_str['wf_unique_id']
    deployment_json = {}

    deployment_response_json = service.Service.deploy_workflow(request, json_str)
    deployment_response_json = json.loads(deployment_response_json)
    #print(deployment_response_json)
    deployment_json['wf_unique_id'] = wf_unique_id
    deployment_json['wf_body'] = deployment_response_json['nodes']
    deployment_json['wf_evaluation_metrics'] = deployment_response_json['wf_evaluation_metrics']
    deployment_json['wf_feature_importance'] = deployment_response_json['wf_feature_importance']
    deployment_json['wf_dependency_plots'] = deployment_response_json['wf_dependency_plots']
    deployment_json['wf_inputs'] = deployment_response_json['wf_inputs']
    deployment_json['wf_outputs'] = deployment_response_json['wf_outputs']
    deployment_json['experimentName'] = experimentName
    response = experiment_service.save_deployed_workflow(deployment_json)
    return HttpResponse(response, content_type="application/json")

@csrf_exempt
def get_kaggle_datasets_list(request, page):
    kaggle.api.authenticate()
    datasets = []
    for dataset in kaggle.api.datasets_list(page=page):
        datasets.append({
                "name": dataset['title'],
                "ref": dataset['ref'],
                "type": "string",
                "value": dataset['id']
            })    
    return HttpResponse(json.dumps(datasets), content_type="application/json")
  
  
  

