from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, CenterSettingsAPIView, ImageUploadView

router = DefaultRouter()
router.register("certificate", CertificateViewSet, basename="certificate")

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path("api/settings/", CenterSettingsAPIView.as_view()),
    path("upload/image/", ImageUploadView.as_view(), name="image-upload"),
]
