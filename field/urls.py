from django.urls import include, path

urlpatterns = [
    path("api/", include("field.api.urls")),
]
