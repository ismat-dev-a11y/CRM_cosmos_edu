# views.py
from django.db.models import Avg, Count

from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from drf_spectacular.utils import extend_schema

from .models import Rating
from .serializers import RatingSerializer, RatingUpdateSerializer, TopStudentSerializer
from apps.users.permissions import IsAuthenticatedAndActive, IsMentor, IsStudent, IsAdmin


# ✅ POST /ratings/  — Mentor studentga baho beradi
@extend_schema(tags=["Ratings"], summary="Studentga baho berish (Mentor)")
class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsMentor]  # ✅ Mentor

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)  # ✅ mentor avtomatik saqlanadi


# ✅ GET /ratings/<pk>/
@extend_schema(tags=["Ratings"], summary="Baho detallari")
class RatingRetrieveView(RetrieveAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        user = self.request.user
        if user.role in ["ADMIN", "BOSS"]:
            return Rating.objects.filter(is_active=True)
        if user.role == "MENTOR":
            return Rating.objects.filter(mentor=user, is_active=True)
        if user.role == "STUDENT":
            return Rating.objects.filter(student=user, is_active=True)
        return Rating.objects.none()


# ✅ PATCH /ratings/<pk>/update/  — Mentor o'z bergan bahosini yangilaydi
@extend_schema(tags=["Ratings"], summary="Bahoni yangilash (Mentor)")
class RatingUpdateView(UpdateAPIView):
    serializer_class = RatingUpdateSerializer
    permission_classes = [IsAuthenticatedAndActive, IsMentor]  # ✅ Mentor
    http_method_names = ["patch"]

    def get_queryset(self):
        return Rating.objects.filter(mentor=self.request.user, is_active=True)


# ✅ DELETE /ratings/<pk>/delete/  — Soft delete
@extend_schema(tags=["Ratings"], summary="Bahoni o'chirish")
class RatingDeleteView(DestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        user = self.request.user
        if user.role in ["ADMIN", "BOSS"]:
            return Rating.objects.filter(is_active=True)
        if user.role == "MENTOR":
            return Rating.objects.filter(mentor=user, is_active=True)
        return Rating.objects.none()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


# ✅ GET /ratings/my/  — Student o'ziga berilgan baholarni ko'radi
@extend_schema(tags=["Ratings"], summary="Menga berilgan baholar (Student)")
class MyRatingsView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsStudent]

    def get_queryset(self):
        return Rating.objects.filter(
            student=self.request.user,
            is_active=True
        ).select_related("mentor", "course")


# ✅ GET /ratings/given/  — Mentor o'zi bergan baholarni ko'radi
@extend_schema(tags=["Ratings"], summary="Men bergan baholar (Mentor)")
class MentorGivenRatingsView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsMentor]

    def get_queryset(self):
        return Rating.objects.filter(
            mentor=self.request.user,
            is_active=True
        ).select_related("student", "course")


# ✅ GET /ratings/all/  — Admin hammani ko'radi
@extend_schema(tags=["Ratings"], summary="Barcha baholar (Admin)")
class AllRatingsView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsAdmin]

    def get_queryset(self):
        return Rating.objects.filter(is_active=True).select_related("student", "mentor", "course")


# ✅ GET /ratings/top-students/  — Eng yuqori baholanган studentlar
@extend_schema(tags=["Ratings"], summary="Top studentlar reytingi (Admin)")
class TopStudentsChartView(ListAPIView):
    permission_classes = [IsAuthenticatedAndActive, IsAdmin]
    serializer_class = TopStudentSerializer

    def get_queryset(self):
        return (
            Rating.objects.filter(is_active=True)
            .values("student__id", "student__first_name", "student__last_name")
            .annotate(avg_score=Avg("score"), total_ratings=Count("id"))
            .order_by("-avg_score")
        )