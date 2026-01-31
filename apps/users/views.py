from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import (
    UserProfileSerializers,
    UserVerifyLoginSerializer
)
from .models import UserProfile

class UserVerifyLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializers
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response(
                {"detail": "Phone number and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = UserProfile.objects.get(phone_number=phone_number, password=password)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Invalid creditianals'}, status=401)

        if not user.is_active:
            return Response({'detail': 'User is inactive'}, status=403)

        refresh = RefreshToken.for_user(user)

        return Response({'refresh': str(refresh), "access": str(refresh.access_token), 'role': user.role, 'user_id': user.id})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )