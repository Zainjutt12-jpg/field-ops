from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import LoginHistory, UserType
from admin_portal.api.v1.Serializers.auth_serializers import LoginSerializer
from utils.responses import success


class AdminLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if not user or user.user_type != UserType.ADMIN:
            return Response(
                {"success": False, "message": "Invalid admin credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        LoginHistory.objects.create(
            user=user,
            access_token=access,
            refresh_token=str(refresh),
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
            created_by=user.username,
        )
        return success(
            {
                "access": access,
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "user_type": user.user_type,
                },
            },
            message="Login successful",
        )
