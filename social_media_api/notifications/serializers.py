# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'target', 'timestamp', 'unread')

    def get_actor(self, obj):
        if obj.actor:
            return {'id': obj.actor.id, 'username': obj.actor.username}
        return None

    def get_target(self, obj):
        # Represent target minimally: content type and id, more detail can be added
        if obj.target_content_type and obj.target_object_id:
            return {
                'content_type': obj.target_content_type.model,
                'id': obj.target_object_id
            }
        return None