# local apps
from .serializers import LessonSerializer, CourseReadSerializers, CourseCreateSerializer
from .models import Lesson, Course
from apps.core.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from apps.users.permissions import IsAdmin
from drf_spectacular.utils import extend_schema
from apps.core.pagination import StandardResultsSetPagination

# glo
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny


@extend_schema(
    tags=["Courses"],
    responses={200: CourseReadSerializers(many=True)},
)
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseReadSerializers
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


@extend_schema(tags=["Courses"])
class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

@extend_schema(tags=["Courses"])
class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    parser_classes = (MultiPartParser, FormParser)

# lesson
@extend_schema(tags=["Lessons"])
class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["Lessons"])
class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


@extend_schema(tags=["Lessons"])
class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
