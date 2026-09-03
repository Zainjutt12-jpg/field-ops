from django.urls import include, path

urlpatterns = [
    path("v1/", include("admin_portal.api.v1.urls")),
]
