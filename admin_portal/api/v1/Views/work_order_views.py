from rest_framework.views import APIView

from accounts.models import User, UserType
from common.Permissions import IsAdminUserType
from common.pagination import StandardResultSetPagination
from operations.api.v1.Serializers.work_order_serializers import (
    WorkOrderAssignSerializer,
    WorkOrderSerializer,
)
from operations.CommonLogics.work_order_logic import WorkOrderLogic
from operations.models import WorkOrder
from utils.responses import success


class AdminWorkOrderListView(APIView):
    permission_classes = [IsAdminUserType]

    def get(self, request):
        qs = WorkOrder.objects.select_related(
            "client", "status", "service_type", "region", "assigned_to"
        ).all()
        status_code = request.query_params.get("status")
        if status_code:
            qs = qs.filter(status__code=status_code)
        paginator = StandardResultSetPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        return paginator.get_paginated_response(WorkOrderSerializer(page, many=True).data)


class AdminWorkOrderAssignView(APIView):
    permission_classes = [IsAdminUserType]

    def post(self, request, reference):
        work_order = WorkOrder.objects.filter(reference=reference).first()
        if not work_order:
            return success(message="Work order not found", status=404)
        serializer = WorkOrderAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tech = User.objects.filter(
            username=serializer.validated_data["technician_username"],
            user_type=UserType.FIELD,
        ).first()
        if not tech:
            return success(message="Technician not found", status=404)
        work_order = WorkOrderLogic.assign(work_order, tech, request.user.username)
        return success(WorkOrderSerializer(work_order).data, message="Assigned")
