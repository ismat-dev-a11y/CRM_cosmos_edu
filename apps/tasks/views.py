# core/views.py
from rest_framework import generics, permissions
from .models import DailyTask
from .serializers import DailyTaskSerializer
from apps.users.permissions import IsAdmin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.users.permissions import IsMentor

class DailyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsMentor]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return DailyTask.objects.all()
        return DailyTask.objects.filter(assigned_to=user) 
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

class MarkHomeWork(generics.CreateAPIView):
    queryset = DailyTask.objects.all()
    serializer_class = DailyTaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsMentor]