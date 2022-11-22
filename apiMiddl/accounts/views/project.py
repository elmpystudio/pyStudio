from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers.project import *

class ProjectView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectWriteSerializer
        else:
            return ProjectReadSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(collaborators=user)

