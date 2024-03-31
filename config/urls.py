# -*- coding: utf-8 -*-
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information
    please see: https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include,
    path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path
from ninja_extra import NinjaExtraAPI
from config import settings
from src.games.api import CatalogController, GamesController
from src.main.api import MainController
from src.orders.api import OrderController
from src.products.api import ProductController
from src.users.api import AuthController, CustomTokenObtainPairController, UsersController
from ninja.errors import AuthenticationError, ValidationError
from django.utils.translation import gettext as _
from ninja_extra import status

main_api = NinjaExtraAPI()


@main_api.exception_handler(AuthenticationError)
def user_unauthorized(request, exc):
    return main_api.create_response(
        request,
        {"message": _("Unauthorized")},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@main_api.exception_handler(ValidationError)
def http_exceptions_handler(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    """
    Handle all Validation errors.
    """
    error_list = []
    for error in exc.errors:
        location = error["loc"][0]
        field_full = ".".join(map(str, error["loc"][1:])) if len(error["loc"]) > 1 else None
        message = _(error["msg"])
        error_list.append(
            {
                "location": location,
                "field": field_full,
                "message": message.capitalize(),
            }
        )

    return main_api.create_response(
        request,
        data={
            "error": {
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "details": error_list
            },
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


# main_api.register_controllers(NinjaJWTDefaultController)
main_api.register_controllers(CustomTokenObtainPairController)
main_api.register_controllers(ProductController)
main_api.register_controllers(OrderController)
main_api.register_controllers(UsersController)
main_api.register_controllers(AuthController)
main_api.register_controllers(GamesController)
main_api.register_controllers(CatalogController)
main_api.register_controllers(MainController)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", main_api.urls),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
