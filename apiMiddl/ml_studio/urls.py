from django.urls import path, re_path
from . import views

app_name = 'machine_learning_app'
urlpatterns = [

    # ok
    re_path(r'^nodes/get_kaggle_datasets_list', views.get_kaggle_datasets_list, name='get_kaggle_datasets_list'),
    re_path(r'^nodes/list', views.get_nodes_list, name='get_nodes_list'),
    re_path(r'^workflow/execute/', views.execute_workflow, name='execute_workflow'),
    re_path(r'^workflow/progress/(?P<workflow_id>\w+)/$', views.get_workflow_progress, name='get_workflow_progress'),
    re_path(r'^node/output/', views.get_node_output, name='get_node_output'),
    re_path(r'^node/get_workflow_ports_md/', views.get_node_metadata, name='get_node_metadata'),
    re_path(r'^node/get_node_output_pairwise/', views.get_output_pairwise, name='get_output_pairwise'),
    re_path(r'^node/get_node_output_corr_matrix/', views.get_output_corr_matrix, name='get_output_corr_matrix'),
    re_path(r'^node/get_node_output_hist/', views.get_output_histogram, name='get_output_histogram'),

    # some kinf od tmp error
    re_path(r'^node/get_eval_metrics/', views.get_eval_metrics, name='get_eval_metrics'),
    re_path(r'^node/get_roc_chart/', views.get_roc_chart, name='get_roc_chart'),
    re_path(r'^node/get_model_info/', views.get_model_info, name='get_model_info'),
    re_path(r'^experiment/create/', views.create_experiment, name='create_experiment'),
    re_path(r'^experiment/listByUserId/', views.get_experiments_by_userId, name='get_experiments_by_userId'),
    re_path(r'^experiment/save/', views.save_workflow, name='save_workflow'),
    re_path(r'^experiment/retrieve/', views.retrieve_workflow_by_experimentId, name='retrieve_workflow_by_experimentId'),
    re_path(r'^workflow/deploy/', views.deploy_workflow, name='deploy_workflow'),

]
