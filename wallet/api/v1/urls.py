from django.urls import path

from wallet.api.v1.Views.payout_views import (
    PayoutApproveView,
    PayoutListCreateView,
    PayoutSubmitView,
)

urlpatterns = [
    path("payouts/", PayoutListCreateView.as_view(), name="wallet-payouts"),
    path("payouts/<int:pk>/submit/", PayoutSubmitView.as_view(), name="wallet-payout-submit"),
    path("payouts/<int:pk>/approve/", PayoutApproveView.as_view(), name="wallet-payout-approve"),
]
