# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("assignments", AssignmentViewSet, basename="assignment")
# router.register("assignment", AssignmentViewSet)

urlpatterns = [
    path("enrollment", EnrollmentCreateAPIView.as_view()),
    path("enrollment", EnrollmentListAPIView.as_view()),
    path("enrollment/<int:pk>", EnrollmentUpdateDeleteAPIView.as_view()),
    path("attendence", AttendenceAPIView.as_view()),
    path("attendence", AttendenceListAPIView.as_view()),
    path("attendence/<int:pk>", updateattendence),
    path("", include(router.urls)),
    # path("" ,include(router.urls)),
]
