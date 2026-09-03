from rest_framework import serializers

from catalog.models import Region, ServiceType


class PublicWorkOrderCreateSerializer(serializers.Serializer):
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
