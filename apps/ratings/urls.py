# urls.py
from django.urls import path
from .views import (
    RatingCreateView,
    RatingRetrieveView,
    RatingUpdateView,
    RatingDeleteView,
    MyRatingsView,
    MentorGivenRatingsView,
    AllRatingsView,
    TopStudentsChartView,
)

urlpatterns = [
    # ✅ Avval specific URL lar
    path("ratings/my/",              MyRatingsView.as_view(),          name="my-ratings"),
    path("ratings/given/",           MentorGivenRatingsView.as_view(), name="mentor-given-ratings"),
    path("ratings/all/",             AllRatingsView.as_view(),         name="all-ratings"),
    path("ratings/top-students/",    TopStudentsChartView.as_view(),   name="top-students"),

    # ✅ Keyin dynamic pk
    path("ratings/",                 RatingCreateView.as_view(),       name="rating-create"),
    path("ratings/<int:pk>/",        RatingRetrieveView.as_view(),     name="rating-retrieve"),
    path("ratings/<int:pk>/update/", RatingUpdateView.as_view(),       name="rating-update"),
    path("ratings/<int:pk>/delete/", RatingDeleteView.as_view(),       name="rating-delete"),
]