from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserList

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path('users/', UserList.as_view())
]