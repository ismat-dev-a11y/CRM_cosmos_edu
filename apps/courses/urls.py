from django.urls import path
from .views import *

urlpatterns = [
    path("course/", CourseListView.as_view()),
    path("create-course/", CourseCreateView.as_view()),
    path("course/<int:pk>", CourseDetailAPIView.as_view()),
    path("lesson", LessonListView.as_view()),
    path("lesson/", LessonCreateView.as_view()),
    path("lesson/<int:pk>", LessonRetrieveUpdateDestroyAPIView.as_view()),
]