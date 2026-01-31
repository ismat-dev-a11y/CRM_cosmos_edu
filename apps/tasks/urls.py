from django.urls import path, include
from .views import DailyTaskListCreateView, MarkHomeWork


urlpatterns = [
    path('', DailyTaskListCreateView.as_view()),
    path('completed/<int:pk>/', MarkHomeWork.as_view())
]
