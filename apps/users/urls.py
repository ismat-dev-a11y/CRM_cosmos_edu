from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("auth/login/", views.UserVerifyLogin.as_view()),
    # path('update/account/<int:pk>', views.UserProfileUpdateView.as_view())
]
