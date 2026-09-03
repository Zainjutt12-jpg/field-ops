from django.urls import path

from client_portal.api.v1.Views.auth_views import ClientLoginView
from client_portal.api.v1.Views.work_order_views import ClientWorkOrderListCreateView

urlpatterns = [
    path("auth/login/", ClientLoginView.as_view(), name="client-login"),
    path("work-orders/", ClientWorkOrderListCreateView.as_view(), name="client-work-orders"),
]
