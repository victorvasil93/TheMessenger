from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message
import datetime


class MessageSerializer(serializers.Serializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    subject = serializers.CharField(max_length=1000)
    creation_date = serializers.DateTimeField(default=datetime.datetime.now())
    is_read = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
