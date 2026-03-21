from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserList, StaffRegisterView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path('users/', UserList.as_view()),
    path('staff/register/', StaffRegisterView.as_view(), name='staff-register')
]