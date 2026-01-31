from rest_framework import viewsets, permissions, generics
# local
from .models import Room, GroupStudent, Group
from .serializers import RoomSerializers, GroupStudentSerializers, GroupSerializer
from apps.users.permissions import IsAdmin, IsMentor

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsMentor | IsAdmin]

        return [permission() for permission in permission_classes]

class GroupViewSet(viewsets.ModelViewSet):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Group.objects.all()
    return Group.objects.filter(mentor=user)

  def get_permissions(self):
    if self.action in ['create', 'destroy']:
      permission_classes = [permissions.IsAuthenticated, IsAdmin]
    else:
      permission_classes = [permissions.IsAuthenticated, IsMentor | IsAdmin]
    return [permission() for permission in permission_classes]
