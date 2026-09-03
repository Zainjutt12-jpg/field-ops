from rest_framework import serializers

from catalog.models import Region, ServiceType, WorkOrderStatus
from operations.models import WorkOrder


class WorkOrderSerializer(serializers.ModelSerializer):
    status_code = serializers.CharField(source="status.code", read_only=True)
    service_type_code = serializers.CharField(source="service_type.code", read_only=True)
    region_code = serializers.CharField(source="region.code", read_only=True)
    client_code = serializers.CharField(source="client.code", read_only=True)
    assigned_to_username = serializers.CharField(source="assigned_to.username", read_only=True, default=None)

    class Meta:
        model = WorkOrder
        fields = [
            "public_id",
            "reference",
            "title",
            "description",
            "address",
            "scheduled_for",
            "completed_at",
            "status_code",
            "service_type_code",
            "region_code",
            "client_code",
            "assigned_to_username",
            "created_at",
        ]


class WorkOrderCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    address = serializers.CharField(required=False, allow_blank=True, default="")
    scheduled_for = serializers.DateTimeField(required=False, allow_null=True)
    service_type_code = serializers.SlugRelatedField(
        slug_field="code", queryset=ServiceType.objects.all(), source="service_type"
    )
    region_code = serializers.SlugRelatedField(
        slug_field="code", queryset=Region.objects.all(), source="region"
    )


class WorkOrderAssignSerializer(serializers.Serializer):
    technician_username = serializers.CharField()
