from rest_framework.views import APIView

from common.Permissions import IsFieldUserType
from common.pagination import StandardResultSetPagination
from operations.api.v1.Serializers.work_order_serializers import WorkOrderSerializer
from operations.CommonLogics.work_order_logic import WorkOrderLogic
from operations.models import WorkOrder
from utils.responses import success


class FieldMyWorkOrdersView(APIView):
    permission_classes = [IsFieldUserType]

    def get(self, request):
        qs = WorkOrder.objects.select_related(
            "status", "service_type", "region", "client"
        ).filter(assigned_to=request.user)
        paginator = StandardResultSetPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        return paginator.get_paginated_response(WorkOrderSerializer(page, many=True).data)


class FieldCompleteWorkOrderView(APIView):
    permission_classes = [IsFieldUserType]

    def post(self, request, reference):
        work_order = WorkOrder.objects.filter(reference=reference, assigned_to=request.user).first()
        if not work_order:
            return success(message="Work order not found", status=404)
        work_order = WorkOrderLogic.complete(work_order, request.user.username)
        return success(WorkOrderSerializer(work_order).data, message="Completed")
