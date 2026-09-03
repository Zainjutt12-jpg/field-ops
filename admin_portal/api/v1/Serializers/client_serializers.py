from rest_framework import serializers

from operations.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "code", "name", "contact_email", "is_active", "api_token", "created_at"]
        read_only_fields = ["api_token", "created_at"]


class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["code", "name", "contact_email", "is_active"]
