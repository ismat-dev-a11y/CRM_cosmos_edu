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
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('courses/', include('apps.courses.urls')),
    path('enrollments/', include('apps.enrollments.urls')),
    path('ratings/', include('apps.ratings.urls')),
    path('payments/', include('apps.payments.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('groups/', include('apps.groups.urls')),
    path('core/', include('apps.core.urls')),
    path('tasks/', include('apps.tasks.urls')),

    # for web socket
    path('', TemplateView.as_view(template_name='chat.html')),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
