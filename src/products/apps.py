# -*- coding: utf-8 -*-
"""
    Application configuration for the products Django app.
"""
from celery.utils.dispatch.signal import Signal
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Application configuration for the products Django app.

    This class defines configuration settings for the products Django app.
    It provides metadata about the app, such as the app's verbose name and
    any default configurations. It can also include signals to be executed
    when the app is ready or when it is being shut down.

    Usage:
        To use this configuration class, ensure that it is set as the default
        AppConfig for the app in the app's __init__.py file:

        ```
        default_app_config = 'myapp.apps.MyAppConfig'
        ```

    For more information on AppConfigs, see the Django documentation:
    https://docs.djangoproject.com/en/stable/ref/applications/#configuring-applications
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.products"

