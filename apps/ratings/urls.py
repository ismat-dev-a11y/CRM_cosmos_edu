from django.urls import path
from .views import *

urlpatterns = [
    path("ratings/", RatingCreateView.as_view(), name="rating-create"),
    path("ratings/<int:pk>/", RatingDetailView.as_view(), name="rating-detail"),

    path("ratings/my/", MyRatingsView.as_view(), name="my-ratings"),
    path("ratings/given/", MentorGivenRatingsView.as_view(), name="mentor-ratings"),

    path("ratings/top-students/", TopStudentsChartView.as_view(), name="top-students"),
]
