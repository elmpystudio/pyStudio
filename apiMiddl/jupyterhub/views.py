from django.shortcuts import redirect
import urllib.request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Jupyter, Jupyter_history
from django.utils.crypto import get_random_string
from accounts.models import CustomUser
from datasets.models import Dataset
import os

def upload_datasets(user):
    container_name = "jupyter-"+user.username
    datasets = Dataset.objects.filter(user=user)
    tmp = "/tmp/api/jupyterhub/"+user.username
    os.system("mkdir -p "+tmp)
    for dataset in datasets:
        file = tmp+"/"+dataset.filename
        dataset.download(file)
        os.system("docker cp " + file + " " + container_name + ":/home/jovyan")

    # clean server /tmp
    os.system("rm -r " + tmp)

@api_view(['GET'])
@permission_classes((AllowAny, ))   
def startView(request):
    token = request.GET.get("token")

    user = CustomUser.objects.filter(jhub_token=token)[0]
    history = Jupyter_history.objects.create(user=user)
    history.save()

    # open auth
    jupyter = Jupyter.objects.get(pk=1)
    jupyter.is_open = True
    jupyter.save()

    try:
        upload_datasets(user)
    except Exception as e:
        print(e)

    return redirect("http://localhost:9000/hub/login")

    # debugging zone
    # print('Start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # print(request.GET.get("username"))
    # print('Start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # return

@api_view(['GET'])
@permission_classes((AllowAny, ))   
# get client_id call => return user code [generate from register]
def authorizeView(request):
    # debugging zone
    # print('Auth!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # print(request.GET.get('state'))
    # print('Auth!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # return
    
    # full response 
    # {
    #     "response_type":"code",
    #     "redirect_uri":"http:\/\/192.168.33.10:8070\/oauth_callback",
    #     "client_id":"ff1b50763d51ec2eb2ace8e76e57099ca215b18629fecab0d33a6e51fd29d8b4",
    #     "state":"eyJzdGF0ZV9pZCI6ICIxNmY4ODIzNzIwNTg0MjdhYTcxMDdmNTI2OGViYjQ0ZiIsICJuZXh0X3VybCI6ICIvaHViLyJ9"
    # }

    # check auth is_open
    jupyter = Jupyter.objects.get(pk=1)
    if not jupyter.is_open:
        return JsonResponse({"error": "Unauthorize"}, safe=False)

    client_id = "QmS4c2KSGvU$45OwlYV2JshEuUG0TO0XTzr1hB3E7"
    # check if client_it is match
    if client_id != request.GET.get('client_id'):
        return JsonResponse({"error": "Authorize Error"}, safe=False)
    
    # redirect url
    url = request.GET.get('redirect_uri')
    url += "?response_type=" + request.GET.get('response_type')
    url += "&client_id=" + request.GET.get('client_id')
    url += "&state=" + request.GET.get('state')
    url += "&code=12345"

    return redirect(url)

    

@csrf_exempt
@permission_classes((AllowAny, ))   
def loginView(request):

    history = Jupyter_history.objects.all()
    last_history = history[Jupyter_history.objects.count()-1]

    data = {
        "access_token": last_history.user.jhub_token,
        "expires_in": 3600,
        "token_type": "bearer"
    }

    return JsonResponse(data, safe=False)

    # debugging zone
    # print('Login!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # print(request.POST)
    # print('Login!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # return

@api_view(['GET'])
@permission_classes((AllowAny, ))
def userView(request):

    token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
    user = CustomUser.objects.filter(jhub_token=token)[0]

    # close auth
    jupyter = Jupyter.objects.get(pk=1)
    jupyter.is_open = False
    jupyter.save()

    return JsonResponse({
        "username": user.username    
    }, safe=False)

    # debugging zone
    # print('User!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # print(token)
    # print('User!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') # test
    # return