from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import UserProfile
from .serializers import RegisterSerializer, LoginSerializer, UserListSerializers, StaffRegisterSerializer


# ================= REGISTER API =================
@extend_schema(tags=["Authentication"])
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Api - Auth"],
        summary="Talaba ruyhatdan o'tkazish",
        description="Talabani ro'yxatdan o'tkazadi, guruhga qo'shadi va ota-onasini bog'laydi.",
        request=RegisterSerializer,

    )

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id"      : user.id,
                    "fullName": user.full_name(),
                    "phone"   : user.phone_number,
                    "role"    : user.role,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= LOGIN API =================

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Api - Auth"],
        summary="Login with phone and password",
        description="Authenticates user, sets is_active=True and returns JWT tokens.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful"),
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Phone or password is incorrect"),
        },
    )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        return Response({
            "message": "Login successful",
            "access": data["access"],
        }, status=status.HTTP_200_OK)

class UserList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]

class StaffRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    summary="Tutor yoki Admin yaratish",
    description="Faqat super_admin yarata oladi.",
    request=StaffRegisterSerializer,
    responses={201: StaffRegisterSerializer},  
    tags=["Api - Auth"],
)
    def post(self, request):
        # Faqat super_admin ruxsat
        if request.user.role != UserProfile.Role.BOSS:
            return Response(
                {"error": "Sizda bu amalni bajarish uchun ruxsat yo'q."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StaffRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id"      : user.id,
                    "fullName": user.full_name,
                    "phone_number"   : user.phone_number,
                    "role"    : user.role,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)