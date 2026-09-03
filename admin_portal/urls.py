from django.urls import include, path

urlpatterns = [
    path("api/", include("admin_portal.api.urls")),
]
