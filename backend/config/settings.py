"""
Django 프로젝트의 백엔드 및 프론트엔드 기본 설정 파일
현재 기준
- BE: DJango
- FE: React 전제
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# =========================
# Base Directory
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Environment Variables
# =========================

load_dotenv(BASE_DIR / ".env")


# =========================
# Security
# =========================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-culture-call-local-development-key",
)

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1",
).split(",")


# =========================
# Application Definition
# =========================

INSTALLED_APPS = [
    # Django 기본 앱
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party 앱
    "rest_framework",
    "corsheaders",

    # Local apps
    # 앱을 만든 뒤 아래에 추가하면 됩니다.
    # "apps.users",
    # "apps.requests",
    # "apps.creators",
    # "apps.programs",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"


# =========================
# Templates
# =========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# =========================
# Database
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================
# Password Validation
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================
# Internationalization
# =========================

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# =========================
# Static Files
# =========================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================
# Media Files
# =========================

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================
# Default Primary Key Field Type
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================
# Django REST Framework
# =========================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}


# =========================
# CORS
# =========================

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

# 개발 중 임시 허용이 필요하면 아래 값을 True로 바꿀 수 있습니다.
# 단, 배포 시에는 False 권장.
CORS_ALLOW_ALL_ORIGINS = False


# =========================
# AI API Key
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")