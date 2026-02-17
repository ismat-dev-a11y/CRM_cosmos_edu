# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("assignments", AssignmentViewSet, basename="assignment")
# router.register("assignment", AssignmentViewSet)

urlpatterns = [
    path("enrollment/create", EnrollmentCreateAPIView.as_view()),
    path("enrollment/list", EnrollmentListAPIView.as_view()),
    path("update/delete/<int:pk>", EnrollmentUpdateDeleteAPIView.as_view()),
    path("attendence/create", AttendenceAPIView.as_view()),
    path("attendence/list", AttendenceListAPIView.as_view()),
    path("attendence/update/<int:pk>", updateattendence),
    path("", include(router.urls)),
    # path("" ,include(router.urls)),
]
