from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from apps.users.permissions import IsAdmin
from .models import Certificate, CenterSettings
from .serializers import (
    CertificateSerializer, 
    CenterSettingsSerializer
)

class CertificateViewSet(viewsets.ViewSet):
    def create(self, request):
        serializers = CertificateSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificateListApiView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.AllowAny]



from rest_framework.views import APIView

class CenterSettingsAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        settings = CenterSettings.get_settings()
        serializer = CenterSettingsSerializer(settings)
        return Response(serializer.data)

    def patch(self, request):
        settings = CenterSettings.get_settings()
        serializer = CenterSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Sozlamalar saqlandi!"})
        return Response(serializer.errors, status=400)