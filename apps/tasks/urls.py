from django.urls import path
from .views import *

urlpatterns = [

    # TASKS
    path("tasks/", DailyTaskListCreateView.as_view()),

    # HOMEWORK
    path("homework/submit/", HomeworkSubmitView.as_view()),
    path("homework/my/", MySubmissionsView.as_view()),

    # REVIEW
    path("homework/review/", HomeworkReviewCreateView.as_view()),
]
