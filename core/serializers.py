from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Message, Room

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name", "description", "is_private", "created_at", "updated_at"]


class AuthorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MessageSerializer(serializers.ModelSerializer):
    author = AuthorMessageSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "room",
            "author",
        ]
