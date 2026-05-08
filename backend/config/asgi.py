"""
ASGI 인터페이스 구현 파일
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

applications = get_asgi_application()