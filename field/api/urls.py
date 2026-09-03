from django.urls import include, path

urlpatterns = [
    path("v1/", include("field.api.v1.urls")),
]
