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
from datetime import datetime, timedelta

from django.conf.urls.static import static
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.urls import include, path, re_path
from django.utils.translation import gettext as _
from ninja.errors import AuthenticationError, ValidationError
from ninja_extra import NinjaExtraAPI, status
from django.views.generic import ListView, View
from config import settings
from src.games.api import CatalogController, GamesController
from src.main.api import MainController
from src.orders.api import OrderController
from src.orders.models import Order
from src.products.api import ProductController
from src.users.api import AuthController, CustomTokenObtainPairController, UsersController
from django.shortcuts import render

from src.users.models import User
import arrow

class StatisticView(View):
    template_name = 'auth/index.html'

    def get(self, request):
        context = {}

        now = arrow.now()
        now_on_last_week = now - timedelta(days=7)
        start_of_current_week = now.floor('week')
        end_of_current_week = now.ceil('week')
        start_of_last_week = now.floor('week')
        end_of_last_week = now.ceil('week')


        last_7_days = datetime.now() - timedelta(days=7)
        total_users = User.objects.count()
        user_notified = User.objects.filter(notify_me=True).count()
        total_orders = (Order.objects
                        .filter(date_created__gte=last_7_days, status='COMPLETED'))

        total_income = total_orders.aggregate(total=Sum('total_price'))['total']
        context['total_users'] = total_users
        context['notify_me_percent'] = int((user_notified / total_users) * 100)
        context['total_orders'] = total_orders.count()
        context['total_income'] = total_income
        return render(request, self.template_name, context)


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
            "error": {"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "details": error_list},
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


main_api.register_controllers(CustomTokenObtainPairController)
main_api.register_controllers(ProductController)
main_api.register_controllers(OrderController)
main_api.register_controllers(UsersController)
main_api.register_controllers(AuthController)
main_api.register_controllers(GamesController)
main_api.register_controllers(CatalogController)
main_api.register_controllers(MainController)
urlpatterns = [
    path('admin/statistic/', StatisticView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", main_api.urls),
    # path("accounts/", include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
