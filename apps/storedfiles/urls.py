from django.urls import path
from .views import FileUploadView, FileDeleteView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    # path('<int:pk>/delete/', FileDeleteView.as_view(), name='file-delete'),
]