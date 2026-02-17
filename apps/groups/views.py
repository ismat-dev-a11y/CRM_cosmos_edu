from rest_framework import viewsets, permissions, generics

# local
from .models import Room, GroupStudent, Group
from .serializers import RoomSerializers, GroupStudentSerializers, GroupSerializer
from apps.users.permissions import IsAdmin, IsMentor
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Room"])
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsMentor | IsAdmin]

        return [permission() for permission in permission_classes]


@extend_schema(tags=["Groups"])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user

        # admin hammasini ko‘radi
        if user.is_staff:
            return Group.objects.all()

        # faqat list uchun filter
        if self.action == "list":
            return Group.objects.filter(mentor=user)

        # retrieve/update/delete uchun
        return Group.objects.all()


@extend_schema(tags=["Group Students"])
class GroupStudentViewSet(viewsets.ModelViewSet):

    queryset = GroupStudent.objects.select_related(
        "group", "student"
    )

    serializer_class = GroupStudentSerializers

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsMentor | IsAdmin]

        return [permission() for permission in permission_classes]