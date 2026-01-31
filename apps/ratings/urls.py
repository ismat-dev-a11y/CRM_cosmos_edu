# ratings/urls.py
from django.urls import path
from .views import StudentApiView, RatingCreateView, RatingUpdateView

urlpatterns = [
    path('student/<int:student_id>/chart/', StudentApiView.as_view()),
    path('create/rating', RatingCreateView.as_view()),
    path('update/<int:pk>/rating', RatingUpdateView.as_view())
]