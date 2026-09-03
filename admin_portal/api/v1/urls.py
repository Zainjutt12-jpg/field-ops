from django.urls import path

from admin_portal.api.v1.Views.auth_views import AdminLoginView
from admin_portal.api.v1.Views.client_views import ClientDetailView, ClientListCreateView
from admin_portal.api.v1.Views.work_order_views import (
    AdminWorkOrderAssignView,
    AdminWorkOrderListView,
)

urlpatterns = [
    path("auth/login/", AdminLoginView.as_view(), name="admin-login"),
    path("clients/", ClientListCreateView.as_view(), name="admin-clients"),
    path("clients/<str:code>/", ClientDetailView.as_view(), name="admin-client-detail"),
    path("work-orders/", AdminWorkOrderListView.as_view(), name="admin-work-orders"),
    path(
        "work-orders/<str:reference>/assign/",
        AdminWorkOrderAssignView.as_view(),
        name="admin-work-order-assign",
    ),
]
