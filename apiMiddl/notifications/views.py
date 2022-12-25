from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404
from .models import Notification
from .serializers import NotificationSerializerGet, NotificationSerializerPost

class NotificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        notifications = Notification.objects.filter(to_user_id=request.user.id)
        serializer = NotificationSerializerGet(notifications, user=None, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationSerializerPost(data=request.data, user=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NotificationDetail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             data = Notification.objects.filter(to_user_id=self.request.user.id, pk=pk)
#             if len(data) > 0:
#                 return data[0]
#             raise Notification.DoesNotExist
#         except Notification.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         notification = self.get_object(pk)
#         serializer = NotificationSerializerGet(notification, user=None)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         notification = self.get_object(pk)
#         serializer = NotificationSerializerGet(notification, data=request.data, user=None)
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         notification = self.get_object(pk)
#         notification.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationAccept(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Notification.objects.filter(to_user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Notification.DoesNotExist
        except Notification.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        notification = self.get_object(pk)
        notification.dataset.purchased.add(notification.from_user)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationDeny(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            data = Notification.objects.filter(to_user_id=self.request.user.id, pk=pk)
            if len(data) > 0:
                return data[0]
            raise Notification.DoesNotExist
        except Notification.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        notification = self.get_object(pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

