from rest_framework import viewsets, permissions, generics

# local
from .models import Room, GroupStudent, Group
from .serializers import RoomSerializers, GroupStudentSerializers, GroupSerializer
from apps.users.permissions import IsAdmin, IsMentor
from drf_spectacular.utils import extend_schema, OpenApiExample


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

    @extend_schema(
        summary="Guruh yaratish",
        examples=[
            OpenApiExample(
                name="Toq kunlar misoli",
                value={
                    "name": "Python N1",
                    "course": 1,
                    "mentor": 2,
                    "room": 1,
                    "lesson_days": "ODD",   # ODD | EVEN | DAILY
                    "start_time": "09:00",
                    "end_time": "11:00",
                    "start_date": "2026-03-01",
                    "status": "WAITING",
                    "max_students": 12,
                },
                request_only=True,
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Group.objects.all()
        if self.action == "list":
            return Group.objects.filter(mentor=user)
        return Group.objects.all()

@extend_schema(tags=["Group Students"])
class GroupStudentViewSet(viewsets.ModelViewSet):
    queryset = GroupStudent.objects.select_related("group", "student").all()
    serializer_class = GroupStudentSerializers

    @extend_schema(
        summary="Guruhga talaba qo'shish",
        examples=[
            OpenApiExample(
                name="Misol",
                value={
                    "group": 1,
                    "student": 3,
                    "status": "ACTIVE"
                },
                request_only=True,
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)