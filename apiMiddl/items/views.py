
from rest_framework import parsers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import django_filters.rest_framework
from django.http import JsonResponse
import datetime
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
# from utils.TableauWrapper import TableauWrapper

from items.serializers import *


class DetailView(generics.ListAPIView):
    queryset = Item.objects.all()
    permission_classes = (IsAuthenticated,)


class DatasetUpdateView(generics.UpdateAPIView):
    model = Dataset
    queryset = Dataset.objects.all()
    permission_classes = (IsAuthenticated,)

    http_method_names = ['patch']
    lookup_field = 'id'

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'retrieve':
            return DatasetSerializer
        return DatasetUpdateSerializer


class DatasetListCreateView(generics.ListCreateAPIView):
    model = Dataset
    queryset = Dataset.objects.all()
    permission_classes = (IsAuthenticated,)

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id']

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CreateDatasetSerializer
        else:
            return DatasetSerializer


class FileUploadView(generics.CreateAPIView):
    parser_classes = [parsers.MultiPartParser]
    serializer_class = FileUploadSerializer
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request, filename):
        context = {
            "request": self.request,
        }

        request.data['owner'] = self.request.user
        request.data['file'] = self.request.data[filename]
        serializer = FileUploadSerializer(data=request.data, context=context)

        if serializer.is_valid():
            saved_file = serializer.save()
            return JsonResponse({"id": saved_file.id}, status=200)
        return JsonResponse(serializer.errors, status=400)


class VisualAnalyticsView(generics.GenericAPIView):
    queryset = VisualAnalytics.objects.all()
    serializer_class = VisualAnalyticsCreate
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        # input data validation
        input_ser = VisualAnalyticsCreate(data=request.data)
        input_ser.is_valid(raise_exception=True)
        input_data = input_ser.validated_data
        dataset_object = input_data['dataset']
        workbook_name = input_data['name']
        print("We got ds id: " + str(dataset_object.id.id))

        # downloading dataset
        dow_path = "/tmp/" + dataset_object.file.filename

        # tableau part
        """
        t = TableauWrapper()
        proj = user.get_tableau_project()
        ds = t.publish_datasource(proj.id, dow_path, dataset_object.file.filename)
        """

        from utils.random_utils import random_str
        t = TableauWrapper()
        proj = user.get_tableau_project()
        print("Project: " + str(proj))
        wb = t.publish_workbook_with_template_for_db(workbook_name, proj.name, dataset_object, dataset_object.name)

        va = VisualAnalytics.objects.create(dataset=dataset_object, tableau_workbook_id = wb.id, name = workbook_name)
        user.private.add(va.id)

        data = {"id": va.id.id}
        print("Zwrocaony va id: " + str(va.id.id))
        return HttpResponse(JSONRenderer().render(data))


class DatasetSampleView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = ItemDashboardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # mock
        return Item.objects.all()

    def list(self, request, dataset_id):
        d = Dataset.objects.get(id=dataset_id)
        print(d)
        sample_path = "/tmp/sample"
        d.download(sample_path)
        handle = open(sample_path, 'r')
        # handle.readline()
        sample = [handle.readline() for x in range(0, 11)]
        return HttpResponse(JSONRenderer().render({"sample": sample}))


class DatasetRaportHtmlView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = ItemDashboardSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, dataset_id):
        d = Dataset.objects.get(id=dataset_id)
        sci = d.get_science_data_html()
        return HttpResponse(JSONRenderer().render({"raport": sci}))

class DatasetRaportJsonView(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = ItemDashboardSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, dataset_id):
        d = Dataset.objects.get(id=dataset_id)
        sci = d.get_science_data_json()
        return HttpResponse(JSONRenderer().render({"raport": json.loads(sci)}))


class DashboardView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemDashboardSerializer

    def get_queryset(self):
        # mock
        # return Item.objects.all()
        user = self.request.user
        return user.private.all()

    def get_private_items(self):
        items = self.get_queryset()
        # items = self.request.user.purchased.all()
        ret = []
        for item in items:
            form = "--"
            ret.append({
                "id": item.get_item().id.id,
                "name": item.get_item().name,
                "title": item.get_item().name,
                "format": form,
                "uuid": item.get_item().file.uuid,
                "fileName": item.get_item().file.filename,
                "type": item.get_item().display_type_name,
                "last_updated": datetime.datetime.now()
            })
        return ret

    # def get_tableau_vas(self):
    #     t = TableauWrapper()
    #     wbs = t.get_workbooks()
    #     ret = []
    #     for wb in wbs[0]:
    #         ret.append({
    #             "id": wb.id,
    #             "name": wb.name,
    #             "format": "TBX",
    #             "type": "Visual Analytics",
    #             "last_updated": datetime.datetime.now()
    #         })
    #
    #     return ret

    def get_purchased_items(self, request):
        ret = []
        for item in request.user.purchased.all():
            ret.append({
                "id": item.id,
                "name": item.get_item().name,
                "title": item.get_item().name,
                "format": "TBX",
                "type": item.get_item().display_type_name,
                "last_updated": datetime.datetime.now()
            })
        return ret

    def list(self, request, items_type):

        print("----------------")
        print(items_type)
        print("----------------")

        valid_types = ["private", "purchased"]
        if not items_type in valid_types:
            msg = ", ".join(valid_types)
            print(msg)
            return HttpResponse(JSONRenderer().render({"error": "Valid options are: " + msg}))

        if items_type == 'private':
            ret = self.get_private_items()
            #ret.extend(self.get_tableau_vas())
        elif items_type == 'purchased':
            ret = self.get_purchased_items(request)

        # ser = ItemDashboardSerializer(ret, many=True)
        return HttpResponse(JSONRenderer().render(ret))
