from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.api_urls")),
    path("cpanel/", include("admin_portal.urls")),
    path("client/", include("client_portal.urls")),
    path("field/", include("field.urls")),
    path("wallet/", include("wallet.urls")),
    path("api/", include("public_api.api.urls")),
]
