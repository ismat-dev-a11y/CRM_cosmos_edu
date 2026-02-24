from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.courses.urls")),
    path("", include("apps.enrollments.urls")),
    path("", include("apps.ratings.urls")),
    path("", include("apps.payments.urls")),
    path("", include("apps.notifications.urls")),
    path("", include("apps.groups.urls")),
    path("", include("apps.core.urls")),
    path("", include("apps.tasks.urls")),

    # swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# ✅ DEVELOPMENT uchun static + media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)