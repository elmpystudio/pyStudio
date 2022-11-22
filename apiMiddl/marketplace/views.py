from django.shortcuts import render
from .models import Offering
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
#from rest_framework import filters
from rest_framework import filters
import coreapi
from django.http import JsonResponse


class TagFilter(filters.BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='tags',
            location='query',
            required=False,
            type='string'
        )]

    def filter_queryset(self, request, qs, view):
        tags = request.query_params.get("tags", None)
        if tags:
            for tag in tags.split(","):
                qs = qs.filter(tags__name=tag)
        return qs

class IdFilter(filters.BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='id',
            location='query',
            required=False,
            type='integer'
        )]

    def filter_queryset(self, request, qs, view):
        id = request.query_params.get("id", None)
        if id:
            qs = qs.filter(id=id)
        return qs

# creating va offer
class OfferingView(generics.ListCreateAPIView):

    queryset = Offering.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [TagFilter, IdFilter]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WriteOfferingSerializer
        else:
            return ReadOfferingSerializer

class DashboardView(generics.ListAPIView):

    queryset = Offering.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WriteOfferingSerializer
        else:
            return ReadOfferingSerializer

class PurchaseView(generics.GenericAPIView):

    serializer_classs = PurchaseSerializer
    queryset = Offering.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return PurchaseSerializer

    def post(self, request):
        input_ser = self.get_serializer(data=request.data)
        input_ser.is_valid(raise_exception=True)
        input_data = input_ser.validated_data

        offering = input_data['offering']
        user = request.user

        item_type = offering.item.__class__.__name__

        if item_type == "Dataset":
            new_id = user.purchased.add(offering.item)
            user.save()

        elif item_type == "VisualAnalytics":

            print("Tableau purchase")
            wb_id = offering.item.tableau_workbook_id
            from utils.TableauWrapper import TableauWrapper as Tab
            t = Tab()
            dest_project = user.email
            source_wb = t.get_workbook_by_id(wb_id)
            t.copy_workbook(source_wb.name, source_wb.name, dest_project)

        return JsonResponse({"result": "ok"}, status=200)
