from django.urls import include, path

urlpatterns = [
    path("v1/", include("public_api.api.v1.urls")),
]
