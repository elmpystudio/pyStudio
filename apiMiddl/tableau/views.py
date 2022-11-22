from django.shortcuts import render
from items.models import *
# from utils.TableauWrapper import TableauWrapper
from tableau.serializers import *
from rest_framework import generics, viewsets, views
from django.http import JsonResponse
from django.conf import settings
from ipware import get_client_ip
import shutil
import docker
import os


# doublecheck your engine path
USER_DATASETS_ = '/Users/egomicia/projects/new_analytics_engine/user/datasets/'
USER_MODELS_ = '/Users/egomicia/projects/new_analytics_engine/user/models/'


class TableauWorkbooksView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTableauWorkbook
        else:
            return ListTableauWorkbook

    # def list(self, request):
    # t = TableauWrapper()
    # key = t.get_workbooks()

    # print(t.populate_preview_image(key[0][0]))
    # print(key)
    # return JsonResponse({"result":True, "workbooks": [ {"name": key[0][x].name, "id": key[0][x].id} for x in range(0, len(key[0]) )]})

    # def create(self, request):
    # ser = CreateTableauWorkbook(request.data)
    # if ser.is_valid():
    #     ser.save()

# not working as no Tablue licence provided
class TableauKeyView(generics.CreateAPIView):
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated,)
    # serializer_class = ListTableauKey

    def create(self, request):
        input_ser = self.get_serializer(data=request.data)
        input_ser.is_valid()
        input_data = input_ser.validated_data

        ip = input_data['ip']

        print("Trusted ticket for ip: " + ip)


        # key = TableauWrapper.get_trusted_ticket(settings.TABLEAU_SERVER['ADMIN_LOGIN'], ip).decode()

        # here we were doing some file handling that it is just for testing purposes
        # user = request.user
        # key = user.get_tableau_trusted_ticket()
        #
        # shutil.rmtree(USER_DATASETS_)
        # os.mkdir(USER_DATASETS_)
        # shutil.rmtree(USER_MODELS_)
        # os.mkdir(USER_MODELS_)
        #
        # user = self.request.user
        # print("user: " + str(user.username))
        # allfiles = user.private.all()
        # allModels = user.getAllModels(user.username)
        # client = docker.from_env()
        # container = client.containers.get("jupyter-" + str(user.username))
        # path = '/home/jovyan/work/'
        # for f in allfiles:
        #     d = Dataset.objects.get(id=f.id)
        #     d.download(USER_DATASETS_ + d.file.filename)
        #
        # os.system("docker cp " + USER_DATASETS_ + ". " + container.attrs.get("Config").get("Hostname") + ":" + path + "data/")
        #
        # for f in allModels:
        #     Dataset.download_models(f.object_name, USER_MODELS_+f.object_name+".pkl")
        #
        # os.system("docker cp " + USER_MODELS_ + ". " + container.attrs.get("Config").get("Hostname") + ":" + path + "models/")

        return JsonResponse({"result": key != "-1", "key": key})
