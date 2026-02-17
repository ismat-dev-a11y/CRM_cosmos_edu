from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from drf_spectacular.utils import extend_schema

from .models import Rating
from .serializers import RatingSerializer
from apps.users.permissions import (
    IsAuthenticatedAndActive,
    IsMentor,
    IsStudent,
    IsAdmin,
)


@extend_schema(
    tags=["Ratings"],
    summary="Create rating",
    description="Mentor gives rating to student"
)
class RatingCreateView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsMentor]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)

@extend_schema(
    tags=["Ratings"],
    summary="Retrieve / Update / Delete rating"
)
class RatingDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        user = self.request.user

        # ADMIN / BOSS
        if user.role in ["ADMIN", "BOSS"]:
            return Rating.objects.filter(is_active=True)

        # MENTOR
        if user.role == "MENTOR":
            return Rating.objects.filter(
                mentor=user,
                is_active=True
            )

        # STUDENT
        if user.role == "STUDENT":
            return Rating.objects.filter(
                student=user,
                is_active=True
            )

        return Rating.objects.none()

    # soft delete
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


@extend_schema(
    tags=["Ratings"],
    summary="My ratings (Student)"
)
class MyRatingsView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsStudent]

    def get_queryset(self):
        return Rating.objects.filter(
            student=self.request.user,
            is_active=True
        )

@extend_schema(
    tags=["Ratings"],
    summary="Ratings given by mentor"
)
class MentorGivenRatingsView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedAndActive, IsMentor]

    def get_queryset(self):
        return Rating.objects.filter(
            mentor=self.request.user,
            is_active=True
        )

@extend_schema(
    tags=["Ratings"],
    summary="Top students chart"
)
class TopStudentsChartView(APIView):
    permission_classes = [IsAuthenticatedAndActive, IsAdmin]

    def get(self, request):

        data = (
            Rating.objects.filter(is_active=True)
            .values("student__id", "student__username")
            .annotate(avg_score=Avg("score"))
            .order_by("-avg_score")
        )

        return Response(data)

