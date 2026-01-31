# ratings/views.py
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rating
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import RatingSerializer
from apps.users.permissions import IsMentor


class StudentApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, student_id):
        ratings = Rating.objects.filter(student_id=student_id, is_active=True).select_related('course')
        data = {
            "student_id": student_id,
            "labels": [r.course.name for r in ratings],
            "scores": [float(r.score) for r in ratings]
        }
        return Response(data)

class RatingCreateView(CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class RatingUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(student=self.request.user)