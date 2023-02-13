from django.shortcuts import redirect
import urllib.request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Jupyter_queue
from accounts.models import CustomUser
from datasets.models import Dataset
from django.utils.crypto import get_random_string
from django.conf import settings
import os
import docker
from datetime import datetime, timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# Only one user at a time
def open(request):
    queue = Jupyter_queue.objects.all()
    if len(queue) > 0:
        if queue[0].user.id == request.user.id:
            return Response({"status": "Success", "message": "opened Successfully"}, status=status.HTTP_200_OK)    
        now = datetime.now()
        current = now.strftime("%m/%d/%Y, %H:%M:%S")
        timeout = (queue[0].created_at + timedelta(seconds = 10)).strftime("%m/%d/%Y, %H:%M:%S")
        if current > timeout:
            queue[0].delete()
        else:
            return Response({"status": "Error", "message": "Juputerhub Auth Is Busy"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    Jupyter_queue.objects.create(user=request.user)
    return Response({"status": "Success", "message": "opened Successfully"}, status=status.HTTP_200_OK)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sync(request):
    user = request.user
    container_name = "jupyter-"+user.username

    # Validate if container [Exist] or [Running]
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        if container.attrs['State']['Running'] == False:
            return Response({"status": "Error", "message": "Container Not Running."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception:
        return Response({"status": "Error", "message": "Container Not Exist."}, status=status.HTTP_406_NOT_ACCEPTABLE)

    datasets = Dataset.objects.filter(user=user)
    tmp = "/tmp/api/jupyterhub/"+user.username
    os.system("mkdir -p "+tmp)
    for dataset in datasets:
        filepath = tmp+"/"+dataset.filename
        dataset.download(filepath)
        os.system("docker cp " + filepath + " " + container_name + ":/home/jovyan")
    # clean server /tmp
    os.system("rm -r " + tmp)
    return Response({"status": "Success", "message": "Synced Successfully"}, status=status.HTTP_200_OK)
    

@csrf_exempt
@permission_classes([AllowAny])
def auth_step1(request):    
    if settings.JUPYTERHUB_CLIENT_ID != request.GET.get('client_id'):
        return JsonResponse({"error": "Authorize Error"})
    
    # redirect url
    url = request.GET.get('redirect_uri')
    url += "?response_type=" + request.GET.get('response_type')
    url += "&client_id=" + request.GET.get('client_id')
    url += "&state=" + request.GET.get('state')
    url += "&code=12345"

    return redirect(url)

@csrf_exempt
@permission_classes([AllowAny])
def auth_step2(request):
    TOKEN = get_random_string(length=60)
    queue = Jupyter_queue.objects.all()[0]
    queue.token = TOKEN
    queue.save()
    
    return JsonResponse({
        "access_token": TOKEN,
        "expires_in": 3600,
        "token_type": "bearer"
    })

@csrf_exempt
@permission_classes([AllowAny])
def auth_step3(request):
    TOKEN = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
    queue = Jupyter_queue.objects.filter(token=TOKEN)[0]
    user = queue.user
    queue.delete()

    return JsonResponse({
        "username": user.username 
    })
