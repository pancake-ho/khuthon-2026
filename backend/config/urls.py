# backend/config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def system_check(request):
    return JsonResponse(
        {
            "status": "OK",
            "message": "BE Server is running.",
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/system_check/", system_check, name="system_check"),
    path("api/", include("api.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)