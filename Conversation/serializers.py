from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender= serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Message
        fields = ('sender', 'content', 'timestamp')
