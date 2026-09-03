from django.urls import path

from field.api.v1.Views.auth_views import FieldLoginView
from field.api.v1.Views.work_order_views import (
    FieldCompleteWorkOrderView,
    FieldMyWorkOrdersView,
)

urlpatterns = [
    path("auth/login/", FieldLoginView.as_view(), name="field-login"),
    path("work-orders/mine/", FieldMyWorkOrdersView.as_view(), name="field-my-work-orders"),
    path(
        "work-orders/<str:reference>/complete/",
        FieldCompleteWorkOrderView.as_view(),
        name="field-complete-work-order",
    ),
]
