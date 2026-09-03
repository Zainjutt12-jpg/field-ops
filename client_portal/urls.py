from django.urls import include, path

urlpatterns = [
    path("api/", include("client_portal.api.urls")),
]
