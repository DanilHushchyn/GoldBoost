from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from config import settings
from src.website.api import api

urlpatterns = [
    path("", api.urls),  # <---------- !
]

