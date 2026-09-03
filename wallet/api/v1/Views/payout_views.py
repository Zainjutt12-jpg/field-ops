from rest_framework.views import APIView

from common.Permissions import IsClientUserType
from common.pagination import StandardResultSetPagination
from utils.responses import success
from wallet.api.v1.Serializers.payout_serializers import (
    PayoutCreateSerializer,
    PayoutSerializer,
)
from wallet.api.v1.services.payout_service import PayoutService
from wallet.models import PayoutRequest


class PayoutListCreateView(APIView):
    permission_classes = [IsClientUserType]

    def get(self, request):
        qs = PayoutRequest.objects.filter(client=request.user.client)
        paginator = StandardResultSetPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        return paginator.get_paginated_response(PayoutSerializer(page, many=True).data)

    def post(self, request):
        serializer = PayoutCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payout = PayoutRequest.objects.create(
            client=request.user.client,
            amount=serializer.validated_data["amount"],
            currency=serializer.validated_data.get("currency", "USD"),
            notes=serializer.validated_data.get("notes", ""),
            maker=request.user,
            created_by=request.user.username,
        )
        return success(PayoutSerializer(payout).data, message="Payout drafted", status=201)


class PayoutSubmitView(APIView):
    permission_classes = [IsClientUserType]

    def post(self, request, pk):
        payout = PayoutRequest.objects.filter(pk=pk, client=request.user.client).first()
        if not payout:
            return success(message="Payout not found", status=404)
        payout = PayoutService.submit_for_approval(payout, request.user.username)
        return success(PayoutSerializer(payout).data, message="Submitted for approval")


class PayoutApproveView(APIView):
    permission_classes = [IsClientUserType]

    def post(self, request, pk):
        payout = PayoutRequest.objects.filter(pk=pk, client=request.user.client).first()
        if not payout:
            return success(message="Payout not found", status=404)
        payout = PayoutService.approve(payout, request.user, request.user.username)
        return success(PayoutSerializer(payout).data, message="Approved")
