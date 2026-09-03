from rest_framework import serializers

from wallet.models import PayoutRequest


class PayoutSerializer(serializers.ModelSerializer):
    client_code = serializers.CharField(source="client.code", read_only=True)
    maker_username = serializers.CharField(source="maker.username", read_only=True)

    class Meta:
        model = PayoutRequest
        fields = [
            "id",
            "client_code",
            "amount",
            "currency",
            "status",
            "maker_username",
            "notes",
            "created_at",
        ]


class PayoutCreateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(max_length=3, default="USD")
    notes = serializers.CharField(required=False, allow_blank=True, default="")
