from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import UserProfile
from .serializers import RegisterSerializer, LoginSerializer
from .permissions import IsBossUser


# ================= REGISTER API =================
@extend_schema(tags=["Authentication"])
class RegisterAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsBossUser]

# ================= LOGIN API =================

@extend_schema(tags=["Authentication"])
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = data["user"]

        return Response({
            "message": "Login successful",
            "access": data["access"],
            "refresh": data["refresh"],
            "user_id": user.id,
            "role": user.role,
            "phone_number": user.phone_number,
        }, status=status.HTTP_200_OK)