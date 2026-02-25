from django.urls import path
from .views import (
    CenterSettingsRetrieveView,
    CenterSettingsCreateView,
    CenterSettingsUpdateView,
    CenterSettingsPartialUpdateView,
    CenterSettingsDestroyView,
    ImageUploadView
)

urlpatterns = [
    path('settings/',                 CenterSettingsRetrieveView.as_view(),       name='settings-retrieve'),
    path('settings/create/',          CenterSettingsCreateView.as_view(),          name='settings-create'),
    path('settings/update/',          CenterSettingsUpdateView.as_view(),          name='settings-update'),
    path('settings/partial-update/',  CenterSettingsPartialUpdateView.as_view(),   name='settings-partial-update'),
    path('settings/delete/',          CenterSettingsDestroyView.as_view(),         name='settings-delete'),
    path("upload/image/", ImageUploadView.as_view(), name="image-upload"),
]