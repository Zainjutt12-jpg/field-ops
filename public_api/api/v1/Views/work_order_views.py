from rest_framework.views import APIView

from catalog.models import WorkOrderStatus
from operations.api.v1.Serializers.work_order_serializers import WorkOrderSerializer
from operations.CommonLogics.work_order_logic import WorkOrderLogic
from operations.models import WorkOrder
from public_api.api.v1.Serializers.order_serializers import PublicWorkOrderCreateSerializer
from public_api.permissions import HasClientApiToken
from utils.responses import success


class PublicWorkOrderCreateView(APIView):
    authentication_classes = []
    permission_classes = [HasClientApiToken]

    def post(self, request):
        serializer = PublicWorkOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        client = request.client
        status_obj = WorkOrderStatus.objects.get(code="open")
        work_order = WorkOrder.objects.create(
            reference=WorkOrderLogic.next_reference(client.code),
            client=client,
            service_type=data["service_type"],
            region=data["region"],
            status=status_obj,
            title=data["title"],
            description=data.get("description", ""),
            address=data.get("address", ""),
            scheduled_for=data.get("scheduled_for"),
            created_by=f"api:{client.code}",
        )
        return success(WorkOrderSerializer(work_order).data, message="Work order created", status=201)
