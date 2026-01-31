from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CertificateViewSet,
    CertificateListApiView,
    CenterSettingsAPIView
)

router = DefaultRouter()
router.register(r'certificates', CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
    path('certificate/', CertificateListApiView.as_view()),
    path('api/settings/', CenterSettingsAPIView.as_view()),
]
