"""
Django 기본 상태 확인용 URL과 admit URL을 연결하는 파일
추가적으로 URL에 places 앱을 연결하는 기능 추가
이후 /api/ 경로 파일 추가로 연동 예정
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def system_check(request):
    return JsonResponse(
        {
            'status': 'OK',
            'message': 'BE Server is running.'
        }
    )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/system_check/", system_check, name="system_check"),

    # Places API
    path("api/places/", include("app.places.urls"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)