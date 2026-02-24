import requests
import base64
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.users.permissions import IsAdmin
from drf_spectacular.utils import extend_schema, extend_schema_view
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiTypes
from drf_spectacular.openapi import AutoSchema
import requests
import base64

@extend_schema(
    tags=["Upload"],
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "image": {
                    "type": "string",
                    "format": "binary",
                }
            },
            "required": ["image"]
        }
    }
)
class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image = request.FILES.get("image")
        if not image:
            return Response({"error": "Rasm yuborilmadi"}, status=400)

        image_bytes = image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "2359d64da450ab908b2ba891d9d3c21e",
            "image": image_base64
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            return Response({
                "image_url": response.json()["data"]["url"]
            })

        return Response({
            "error": response.json()
        }, status=400)