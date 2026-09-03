from django.urls import include, path

urlpatterns = [
    path("v1/", include("client_portal.api.v1.urls")),
]
