from django.urls import path
from .views import *

urlpatterns = [

    # CREATE + LIST OWN
    path(
        "payments/",
        PaymentCreateView.as_view(),
        name="payment-create-list",
    ),

    # DETAIL
    path(
        "payments/<int:pk>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),

    # MY PAYMENTS
    path(
        "payments/my/",
        MyPaymentsView.as_view(),
        name="my-payments",
    ),

    # ADMIN STATUS UPDATE
    path(
        "payments/<int:pk>/status/",
        PaymentStatusUpdateView.as_view(),
        name="payment-status-update",
    ),

    # ANALYTICS
    path(
        "payments/stats/",
        PaymentStatsView.as_view(),
        name="payment-stats",
    ),
]
