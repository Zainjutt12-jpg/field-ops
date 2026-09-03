from rest_framework.views import APIView

from catalog.models import WorkOrderStatus
from common.Permissions import IsClientUserType
from common.pagination import StandardResultSetPagination
from operations.api.v1.Serializers.work_order_serializers import (
    WorkOrderCreateSerializer,
    WorkOrderSerializer,
)
from operations.CommonLogics.work_order_logic import WorkOrderLogic
from operations.models import WorkOrder
from utils.responses import success


class ClientWorkOrderListCreateView(APIView):
    permission_classes = [IsClientUserType]

    def get(self, request):
        qs = (
            WorkOrder.objects.select_related("status", "service_type", "region", "client")
            .filter(client=request.user.client)
        )
        paginator = StandardResultSetPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        return paginator.get_paginated_response(WorkOrderSerializer(page, many=True).data)

    def post(self, request):
        if not request.user.client_id:
            return success(message="Client profile missing on user", status=400)
        serializer = WorkOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        status_obj = WorkOrderStatus.objects.get(code="open")
        work_order = WorkOrder.objects.create(
            reference=WorkOrderLogic.next_reference(request.user.client.code),
            client=request.user.client,
            service_type=data["service_type"],
            region=data["region"],
            status=status_obj,
            title=data["title"],
            description=data.get("description", ""),
            address=data.get("address", ""),
            scheduled_for=data.get("scheduled_for"),
            created_by=request.user.username,
        )
        return success(WorkOrderSerializer(work_order).data, message="Work order created", status=201)
