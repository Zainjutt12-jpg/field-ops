from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import LoginHistory, UserType
from admin_portal.api.v1.Serializers.auth_serializers import LoginSerializer
from utils.responses import success


class ClientLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if not user or user.user_type != UserType.CLIENT:
            return Response(
                {"success": False, "message": "Invalid client credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        LoginHistory.objects.create(
            user=user,
            access_token=access,
            refresh_token=str(refresh),
            created_by=user.username,
        )
        return success(
            {
                "access": access,
                "refresh": str(refresh),
                "user": {"id": user.id, "username": user.username, "user_type": user.user_type},
            },
            message="Login successful",
        )
