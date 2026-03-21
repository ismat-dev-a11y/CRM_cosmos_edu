import requests
import base64
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.users.permissions import IsAdmin
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import extend_schema
from .models import Certificate, CenterSettings
from .serializers import CertificateSerializer, CenterSettingsSerializer
from apps.core.pagination import PageNumberPagination
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .models import CenterSettings
from .serializers import CenterSettingsSerializer


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .models import CenterSettings
from .serializers import CenterSettingsSerializer

def get_singleton():
    return CenterSettings.get_settings()

# ✅ GET /settings/
class CenterSettingsRetrieveView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CenterSettingsSerializer

    def get_object(self):
        return get_singleton()


# ✅ POST /settings/create/
class CenterSettingsCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CenterSettingsSerializer

    def create(self, request, *args, **kwargs):
        instance = get_singleton()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ✅ PUT /settings/update/
class CenterSettingsUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CenterSettingsSerializer
    http_method_names = ['put']

    def get_object(self):
        return get_singleton()


# ✅ PATCH /settings/partial-update/
class CenterSettingsPartialUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CenterSettingsSerializer
    http_method_names = ['patch']

    def get_object(self):
        return get_singleton()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


# ✅ DELETE /settings/delete/
class CenterSettingsDestroyView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CenterSettingsSerializer

    def get_object(self):
        return get_singleton()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Sozlamalar o'chirildi."}, status=status.HTTP_204_NO_CONTENT)
