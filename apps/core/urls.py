from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, CenterSettingsAPIView

router = DefaultRouter()
router.register("certificate", CertificateViewSet, basename="certificate")

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path("api/settings/", CenterSettingsAPIView.as_view()),
]
