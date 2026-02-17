from django.urls import path
from .views import *

urlpatterns = [
    path("course/list", CourseListView.as_view()),
    path("course/create", CourseCreateView.as_view()),
    path("course/action/<int:pk>", CourseDetailAPIView.as_view()),
    path("lesson", LessonListView.as_view()),
    path("lesson/create", LessonCreateView.as_view()),
    path("lesson/<int:pk>", LessonRetrieveUpdateDestroyAPIView.as_view()),
]