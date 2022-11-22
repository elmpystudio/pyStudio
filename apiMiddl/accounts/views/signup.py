from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication
)
from rest_framework import generics, viewsets, views
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from django.contrib import auth
from django.http import JsonResponse

from utils.authentication import CsrfExemptSessionAuthentication
from utils.mixins import ReadWriteSerializerMixin
# from utils.TableauWrapper import TableauWrapper
from utils.random_utils import random_str
from accounts.serializers.signup import *
from accounts.models import Project
from django.contrib.auth import authenticate, login

User = get_user_model()

class UserView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=True)
        
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):        
        if self.request.method == 'POST':
            return InputRegisterSerializer
        return OutputLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(self.request)
        user.save()

        # tableau account creation
        #t = TableauWrapper()
        
        # t_role = "Publisher"
        # t_user = "t3st_"+random_str(5)
        # t_password = random_str(10)

        # print("Creating new tableau user: %s %s %s" % ( t_role, t_user, t_password ))
        
        # new_tab_user = t.create_user(t_user, t_password, t_role)

        # if new_tab_user == None:
        #     return JsonResponse({"result": False, "error": "Error while creating tableau user"})
        # if new_tab_user.site_role == "Unlicensed":
        #     return JsonResponse({"result": False, "error": "Created new user in Tableau, but with role Unlicensed!"})
        
        # savind final user object
        # user = serializer.save(self.request)
        # user.tableau_user = t_user
        # user.tableau_password = t_user
        # user.tableau_password = t_password
        # user.save()

        return JsonResponse({"result": True})

class LoginView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):        
        if self.request.method == 'POST':
            return InputLoginSerializer 

        return OutputLoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.get_authenticated_user()
        
        if not user:
            return JsonResponse({"result":False})

        login(request, user)
        return JsonResponse({"result":True})

from rest_framework.decorators import api_view

from rest_framework import viewsets
class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def log(request):
    print(request.user)

    login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
    return Response({"result":True})

