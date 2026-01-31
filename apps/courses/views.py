# local apps
from .serializers import LessonSerializer, CourseReadSerializers, CourseCreateSerializer
from .models import Lesson, Course
from apps.users.permissions import IsAdmin
# glo
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny


class CourseListView(generics.ListAPIView):
  queryset = Course.objects.all()
  serializer_class = CourseReadSerializers
  permission_classes = [AllowAny]

class CourseCreateView(generics.CreateAPIView):
  queryset = Course.objects.all()
  serializer_class = CourseCreateSerializer
  permission_classes = [IsAuthenticated, IsAdmin]

  def perform_create(self, serializer):
    serializer.save()

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Course.objects.all()
  serializer_class = CourseReadSerializers
  permission_classes = [IsAuthenticated, IsAdmin]

  def perform_update(self, serializer):
    serializer.save()

  def perform_destroy(self, instance):
    instance.delete()

# lesson
class LessonListView(generics.ListAPIView):
  queryset = Lesson.objects.all()
  serializer_class = LessonSerializer
  permission_classes = [IsAuthenticated]

class LessonCreateView(generics.CreateAPIView):
  serializer_class = LessonSerializer
  permission_classes = [IsAuthenticated, IsAdmin]

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Lesson.objects.all()
  serializer_class = LessonSerializer
  permission_classes = [IsAuthenticated, IsAdmin]
