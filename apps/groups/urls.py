from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, GroupViewSet, GroupStudentViewSet

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"groups", GroupViewSet, basename="group")
router.register(r"group-students", GroupStudentViewSet, basename="group-students")


urlpatterns = [
    path("", include(router.urls)),
]
