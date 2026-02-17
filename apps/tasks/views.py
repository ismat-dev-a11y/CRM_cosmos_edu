# core/views.py
from rest_framework import generics, permissions
from .models import DailyTask, HomeworkReview, HomeworkSubmission
from drf_spectacular.utils import extend_schema
from .serializers import DailyTaskSerializer, HomeworkSubmissionSerializer, HomeworkReviewSerializer
from apps.users.permissions import IsAdmin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.users.permissions import IsMentor

@extend_schema(tags=["Tasks"])
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

@extend_schema(tags=["Homework"])
class HomeworkSubmitView(generics.CreateAPIView):
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

@extend_schema(tags=["Homework"])
class HomeworkSubmitView(generics.CreateAPIView):
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


@extend_schema(tags=["Homework"])
class HomeworkReviewCreateView(generics.CreateAPIView):
    queryset = HomeworkReview.objects.all()
    serializer_class = HomeworkReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsMentor]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


@extend_schema(tags=["Homework"])
class MySubmissionsView(generics.ListAPIView):
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HomeworkSubmission.objects.filter(
            student=self.request.user
        )

@extend_schema(tags=["Homework"])
class MySubmissionsView(generics.ListAPIView):
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HomeworkSubmission.objects.filter(
            student=self.request.user
        )