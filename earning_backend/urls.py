from django.contrib import admin
from django.urls import path, include

from core.cpx import cpx_wall_url, cpx_postback
from core.views_health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("api/", include("core.urls")),  # keep your existing api routes
    path("api/cpx/wall/", cpx_wall_url),
    path("api/cpx/postback/", cpx_postback),
]
