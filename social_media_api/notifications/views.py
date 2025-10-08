from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # unread first, then newest
        return Notification.objects.filter(recipient=user).order_by('-unread', '-timestamp')


class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()

    def post(self, request, pk):
        user = request.user
        notification = get_object_or_404(Notification, pk=pk, recipient=user)
        if not notification.unread:
            return Response({'detail': 'Already read.'}, status=status.HTTP_200_OK)
        notification.unread = False
        notification.save()
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)