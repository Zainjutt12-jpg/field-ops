from django.urls import path

from public_api.api.v1.Views.work_order_views import PublicWorkOrderCreateView

urlpatterns = [
    path("work-orders/", PublicWorkOrderCreateView.as_view(), name="public-work-orders"),
]
