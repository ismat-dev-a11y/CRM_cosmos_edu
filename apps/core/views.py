from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from apps.users.permissions import IsAdmin
from drf_spectacular.utils import extend_schema, extend_schema_view
import requests
from drf_spectacular.utils import extend_schema
from .models import Certificate, CenterSettings
from .serializers import CertificateSerializer, CenterSettingsSerializer
from apps.core.pagination import PageNumberPagination


@extend_schema_view(
    list=extend_schema(tags=["Certificate"]),
    create=extend_schema(tags=["Certificate"]),
    retrieve=extend_schema(tags=["Certificate"]),
    update=extend_schema(tags=["Certificate"]),
    partial_update=extend_schema(tags=["Certificate"]),
    destroy=extend_schema(tags=["Certificate"]),
)
class CertificateViewSet(ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        """
        Landing page → hamma ko‘radi
        Admin → create/update/delete
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdmin()]


from rest_framework.views import APIView


@extend_schema(tags=["Settings"])
class CenterSettingsAPIView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        # Landing page ham ishlatadi
        if self.request.method == "GET":
            return []
        return [IsAdmin()]

    @extend_schema(
        responses=CenterSettingsSerializer,
        description="Markaz sozlamalarini olish (Landing page uchun)"
    )
    def get(self, request):
        settings_obj = CenterSettings.get_settings()
        serializer = CenterSettingsSerializer(settings_obj)
        return Response(serializer.data)

    @extend_schema(
        request=CenterSettingsSerializer,
        responses=CenterSettingsSerializer,
        description="Markaz sozlamalarini yangilash (Admin)"
    )
    def patch(self, request):
        settings_obj = CenterSettings.get_settings()

        serializer = CenterSettingsSerializer(
            settings_obj,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

import base64
@extend_schema(tags=["Upload"])
class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image = request.FILES.get("image")
        if not image:
            return Response({"error": "Rasm yuborilmadi"}, status=400)

        # Base64 ga o'girish
        image_data = base64.b64encode(image.read()).decode("utf-8")

        # IMGbb ga yuborish
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": "YOUR_IMGBB_API_KEY",  # .env ga qo'ying
                "image": image_data,
            }
        )

        if response.status_code == 200:
            url = response.json()["data"]["url"]
            return Response({"image_url": url}, status=200)

        return Response({"error": "Yuklash xatosi"}, status=400)
