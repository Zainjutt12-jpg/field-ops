from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.api.v1.Serializers.client_serializers import (
    ClientCreateSerializer,
    ClientSerializer,
)
from common.Permissions import IsAdminUserType
from common.pagination import StandardResultSetPagination
from operations.models import Client
from utils.responses import success


class ClientListCreateView(APIView):
    permission_classes = [IsAdminUserType]

    def get(self, request):
        qs = Client.objects.all().order_by("-created_at")
        paginator = StandardResultSetPagination()
        page = paginator.paginate_queryset(qs, request, view=self)
        data = ClientSerializer(page, many=True).data
        return paginator.get_paginated_response(data)

    def post(self, request):
        serializer = ClientCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save(created_by=request.user.username)
        return success(ClientSerializer(client).data, message="Client created", status=201)


class ClientDetailView(APIView):
    permission_classes = [IsAdminUserType]

    def get(self, request, code):
        client = Client.objects.filter(code=code).first()
        if not client:
            return Response({"success": False, "message": "Client not found"}, status=404)
        return success(ClientSerializer(client).data)
