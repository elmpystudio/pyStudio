from register import register, login, about
from project import *
from file_upload import file_upload
from tableau import tab
from dataset import new_dataset
from marketplace import *
from dashboard import *
from va import *
from samples import *
from ml import *
import sys
import requests

r = requests.Session()
r.timeout=30

if True:

    print("NO REGISTER RUN")
    data = {
                "username": "root",
                "email": "root",
                "password": "w2w2w2W@",
                "session": r
            }

else:

    print("---------------")
    print("Register")
    print("---------------")
    data = register(r)
print("---------------")
print("Login")
print("---------------")
login(data)

print("---------------")
print("ML: get nodes")
print("---------------")
ml_get_nodes(data)

print("---------------")
print("ML: ml_start_workflow")
print("---------------")
ml_start_workflow(data)

print("---------------")
print("ML: ml_get_status")
print("---------------")
ml_get_status(data)

print("---------------")
print("ML: ml_get_node_output")
print("---------------")
ml_get_node_output(data)


print("---------------")
print("ML: ml_get_node_metrics")
print("---------------")
ml_get_node_metrics(data)


print("---------------")
print("ML: ml_get_node_roc_chart")
print("---------------")
ml_get_node_roc_chart(data)

print("---------------")
print("ML: ml_get_workflow_ports_md")
print("---------------")
ml_get_workflow_ports_md(data)

print("---------------")
print("ML: ml_get_node_output_pairwise")
print("---------------")
ml_get_node_output_pairwise(data)

print("---------------")
print("ML: ml_get_node_output_corr_matrix")
print("---------------")
ml_get_node_output_corr_matrix(data)

print("---------------")
print("ML: ml_get_node_output_hist")
print("---------------")
ml_get_node_output_hist(data)

print("---------------")
print("ML: ml_exp_listByUserId")
print("---------------")
ml_exp_listByUserId(data)


print("---------------")
print("ML: ml_exp_create")
print("---------------")
ml_get_exp_create(data)

print("---------------")
print("ML: ml_save")
print("---------------")
ml_exp_save(data)

print("---------------")
print("ML: ml_retrive")
print("---------------")
ml_exp_retrieve(data)


sys.exit(0)
print("---------------")
print("About")
print("---------------")
about(data)
#print("---------------")
#print("Create project")
#print("---------------")
#data = create_project(data)
#print("---------------")
#print("Get project")
#print("---------------")
#data = get_project(data)
print("---------------")
print("File uploading")
print("---------------")
data = file_upload(data)
print("---------------")
print("Tableau")
print("---------------")
data = tab(data)
print("---------------")
print("New dataset")
print("---------------")
data = new_dataset(data)
print("---------------")
print("New va")
print("---------------")
data = new_va(data)
print("---------------")
print("New va OFFERING")
print("---------------")
data = mp_set_va_offering(data)
print("---------------")
print("New offering")
print("---------------")
data = mp_set_offering(data)

print("---------------")
print("Get offering")
print("---------------")
data = mp_get_offering(data)

print("---------------")
print("Purchase")
print("---------------")
data = mp_purchase(data)

print("---------------")
print("Get sample data from ss")
print("---------------")
data = ds_get_sample(data)

print("---------------")
print("Get panda raport from ds")
print("---------------")
data = ds_get_raport(data)

print("---------------")
print("Get private dashboard")
print("---------------")
data = db_private(data)

print("---------------")
print("Get purchased dashboard")
print("---------------")
data = db_purchased(data)

print("-------------")
print("---- RUN DONE -----")
print("-------------")
