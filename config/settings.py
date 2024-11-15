# -*- coding: utf-8 -*-
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from enum import Enum
from pathlib import Path

import environ
from django.templatetags.static import static
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# django-environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env.prod"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "modeltranslation",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "debug_toolbar",
    "corsheaders",
    "imagekit",
    "django_extensions",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "ninja_jwt",
    "ninja_jwt.token_blacklist",
    "django_cleanup.apps.CleanupConfig",
    "src.users",
    "src.main",
    "src.products",
    "src.orders",
    "src.games",
    "ninja_extra",
    "meta",
]
AUTH_USER_MODEL = "users.User"
PASSWORD_RESET_TIMEOUT = 1800  # 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Change the token expiration time to 30 minutes
# SESSION_COOKIE_SAMESITE = "None"
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = "None"
SITE_ID = 1
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=25),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=5),
    # For Controller Schemas
    # FOR OBTAIN PAIR
    "TOKEN_OBTAIN_PAIR_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainPairInputSchema",
    "TOKEN_OBTAIN_PAIR_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshInputSchema",
    # FOR SLIDING TOKEN
    "TOKEN_OBTAIN_SLIDING_INPUT_SCHEMA": "ninja_jwt.schema.TokenObtainSlidingInputSchema",
    "TOKEN_OBTAIN_SLIDING_REFRESH_INPUT_SCHEMA": "ninja_jwt.schema.TokenRefreshSlidingInputSchema",
    "TOKEN_BLACKLIST_INPUT_SCHEMA": "ninja_jwt.schema.TokenBlacklistInputSchema",
    "TOKEN_VERIFY_INPUT_SCHEMA": "ninja_jwt.schema.TokenVerifyInputSchema",
}
# django settings.py
NINJA_EXTRA = {
    "THROTTLE_RATES": {
        "repeat": "1/10s",
    }
}
UNFOLD = {
    "SITE_TITLE": "GoldBoost",
    "SITE_HEADER": "GoldBoost",
    "ENVIRONMENT": "src.main.utils.environment_callback",
    # "DASHBOARD_CALLBACK": "src.main.views.dashboard_callback",
    "SITE_URL": "/",
    "LOGIN": {
        "image": lambda request: static("games/imgs/login-bg.jpg"),
    },
    "STYLES": [
        lambda request: static("games/css/summernote-lite.css"),
    ],
    "SCRIPTS": [
        lambda request: static("games/js/jquery-3.7.1.js"),
        lambda request: static("games/js/summernote-lite.js"),
        lambda request: static("games/js/summernote-client.js"),
    ],
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
        },
    },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": "Navigation",
                "separator": True,  # Top border
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": f"{env('MEDIA_URL')}/admin/users/user/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Orders",
                        "icon": "receipt",
                        "link": f"{env('MEDIA_URL')}/admin/orders/order/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Statistic",
                        "icon": "monitoring",
                        "link": f"{env('MEDIA_URL')}/admin/statistic",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Main",
                "separator": True,  # Top border
                "items": [
                    {
                        "title": "Why choose us",
                        "icon": "view_carousel",
                        "link": f"{env('MEDIA_URL')}/admin/main/whychooseus/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "News",
                        "icon": "newspaper",
                        "link": f"{env('MEDIA_URL')}/admin/main/news/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Insta",
                        "icon": "camera",
                        "link": f"{env('MEDIA_URL')}/admin/main/insta/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Promo code",
                        "icon": "featured_seasonal_and_gifts",
                        "link": f"{env('MEDIA_URL')}/admin/main/promocode/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Reviews",
                        "icon": "reviews",
                        "link": f"{env('MEDIA_URL')}/admin/main/review/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Settings",
                        "icon": "settings",
                        "link": f"{env('MEDIA_URL')}/admin/main/setting/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Products",
                "separator": True,  # Top border
                "items": [
                    {
                        "title": "Products",
                        "icon": "category",
                        "link": f"{env('MEDIA_URL')}/admin/products/product/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Frequently bought",
                        "icon": "list_alt",
                        "link": f"{env('MEDIA_URL')}/admin/products/freqbought/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Filters",
                        "icon": "filter_alt",
                        "link": f"{env('MEDIA_URL')}/admin/products/filter/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Tags",
                        "icon": "sell",
                        "link": f"{env('MEDIA_URL')}/admin/products/tag/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Games",
                "separator": True,  # Top border
                "items": [
                    {
                        "title": "Games",
                        "icon": "joystick",
                        "link": f"{env('MEDIA_URL')}/admin/games/game/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Calendars",
                        "icon": "calendar_month",
                        "link": f"{env('MEDIA_URL')}/admin/games/calendar/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Calendar blocks",
                        "icon": "calendar_add_on",
                        "link": f"{env('MEDIA_URL')}/admin/games/calendarblock/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Teams",
                        "icon": "groups_3",
                        "link": f"{env('MEDIA_URL')}/admin/games/team/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Worth look",
                        "icon": "view_carousel",
                        "link": f"{env('MEDIA_URL')}/admin/games/worthlook/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Catalog pages",
                        "icon": "menu_book",
                        "link": f"{env('MEDIA_URL')}/admin/games/catalogpage/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": " ",
                        "link": "#",
                    },
                ],
            },
        ],
    },
}
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SOCIALACCOUNT_AUTO_SIGNUP = True  # This automatically signs up a user after using google to sign in

#
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "src.users.authentication.EmailBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        # "APP": {
        #     'EMAIL_AUTHENTICATION': True,
        #     "client_id": env("GOOGLE_OAUTH_CLIENT_ID"),
        #     "secret": env("GOOGLE_OAUTH_CLIENT_SECRET"),
        #     "key": ""
        # },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    }
}
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = [
#    "access-control-allow-origin",
#    "content-type",
#    "cookie",
# ]
CORS_EXPOSE_HEADERS = [
    "access-control-allow-origin",
    "content-type",
    "cookie",
]
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:1337",
    "http://127.0.0.1:5173",
    "https://gold-boost.netlify.app",
    "http://127.0.0.1",
    "https://goodboost-spacelab.avada-media-dev2.od.ua",
]
ROOT_URLCONF = "config.urls"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
ABSOLUTE_URL = f'{env("MEDIA_URL")}'

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
FRONTEND_URL = env("FRONTEND_URL")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
USE_I18N = True

LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Kiev"

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

LANGUAGES = [
    ("en", "English"),
    ("uk", "Ukrainian"),
]

MODELTRANSLATION_LANGUAGES = ("en", "uk")
# MODELTRANSLATION_FALLBACK_LANGUAGES = {'default': ('en',)}
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = []

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
