from django.urls import path
from .views import *

urlpatterns = [
  path("api/course/list", CourseListView.as_view()),
  path('api/course/create', CourseCreateView.as_view()),
  path('api/course/action/<int:pk>', CourseRetrieveUpdateDestroyAPIView.as_view()),
  path('api/lesson', LessonListView.as_view()),
  path('api/lesson/create', LessonCreateView.as_view()),
  path('api/lesson/<int:pk>', LessonRetrieveUpdateDestroyAPIView.as_view())
]
