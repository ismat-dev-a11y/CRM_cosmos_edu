# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
  path('api/enrollment/create', EnrollmentCreateAPIView.as_view()),
  path('api/enrollment/list', EnrollmentListAPIView.as_view()),
  path('api/update/delete/<int:pk>', EnrollmentUpdateDeleteAPIView.as_view()),

  path('api/attendence/create', AttendenceAPIView.as_view()),
  path('api/attendence/list', AttendenceListAPIView.as_view()),
  path('', include(router.urls)),
  path('api/assignment/action', AssignmentUpdateDeleteAPIView.as_view())
]
