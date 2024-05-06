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
import pendulum
from pendulum.datetime import DateTime
from django.conf.urls.static import static
from django.contrib import admin
from django.db.models import Sum, QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import include, path
from django.utils.translation import gettext as _
from ninja.errors import AuthenticationError, ValidationError
from ninja_extra import NinjaExtraAPI, status
from django.views.generic import View
from config import settings
from src.games.api import CatalogController, GamesController
from src.main.api import MainController
from src.orders.api import OrderController
from src.orders.models import Order
from src.products.api import ProductController
from src.products.models import Product
from src.users.api import (AuthController,
                           CustomTokenObtainPairController,
                           UsersController)
from django.shortcuts import render
from src.users.models import User
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class StatisticView(SuperUserRequiredMixin, View):
    template_name = 'statistic/index.html'

    @staticmethod
    def progress_calc(first_number: int, second_number: int) -> float:
        if first_number is None:
            first_number = 0
        if second_number is None:
            second_number = 0
        if second_number <= 0:
            return 0
        return ((first_number / second_number) * 100) - 100

    @staticmethod
    def chart_calc(start: DateTime, num_days: int,
                   orders: QuerySet) -> (float, [], []):
        week_days = []
        week_income_chart = []
        week_icome = 0
        date = start
        for item in range(1, num_days + 2):
            day = date.format('DD dddd')
            week_days.append(day)
            filtered_orders = orders.filter(date_created__date=date.date())
            income = filtered_orders.aggregate(price=Sum('total_price'))['price']
            if income is None:
                income = 0
            income = round(income, 2)
            week_icome = week_icome + income
            week_income_chart.append([1, income])
            date = start.add(days=item)
        return week_icome, week_days, week_income_chart

    def get(self, request):
        context = {}

        today = pendulum.now(tz='Europe/Kiev')
        start_current_week = today.start_of('week')
        end_current_week = today.end_of('week')
        start_last_week = start_current_week.subtract(days=7)
        end_last_week = end_current_week.subtract(days=7)
        total_users = User.objects.count()
        user_notified = User.objects.filter(notify_me=True).count()
        orders_last_week = (Order.objects
        .filter(
            date_created__range=[start_last_week,
                                 end_last_week],
            status='COMPLETED'))
        orders_current_week = (Order.objects
        .filter(
            date_created__range=[start_current_week, end_current_week],
            status='COMPLETED'))
        orders_progress = self.progress_calc(orders_current_week.count(),
                                             orders_last_week.count())

        income_current_week = orders_current_week.aggregate(price=Sum('total_price'))['price']
        income_last_week = orders_last_week.aggregate(price=Sum('total_price'))['price']
        income_progress = self.progress_calc(income_current_week,
                                             income_last_week)

        num_days = end_last_week.diff(start_last_week).in_days()
        last_week_icome, last_week_days, last_week_income_chart = (
            self.chart_calc(start=start_last_week,
                            num_days=num_days,
                            orders=orders_last_week))

        num_days = today.diff(start_current_week).in_days()
        current_week_icome, current_week_days, current_week_income_chart = (
            self.chart_calc(start=start_current_week,
                            num_days=num_days,
                            orders=orders_current_week))

        #pie Chart
        orders_2_last_week = (Order.objects
                              .prefetch_related('items')
                              .filter(date_created__range=
                                      [start_last_week, end_current_week],
                                      status='COMPLETED'))
        list_ids = set()
        for order in orders_2_last_week:
            order: Order
            for item in order.items.all():
                if item.product:
                    list_ids.add(item.product.id)
                if item.freqbot:
                    for prod in item.freqbot.products.all():
                        list_ids.add(prod.id)
        trend_products = Product.objects.filter(id__in=list_ids)[:10]
        trend_chart = []
        for product in trend_products:
            trend_chart.append([product.title, product.bought_count])
        context['trend_chart'] = trend_chart
        context['current_week_icome'] = 0 if current_week_icome is None else round(current_week_icome, 2)
        context['current_week_days'] = current_week_days
        context['current_week_income_chart'] = current_week_income_chart
        context['last_week_icome'] = 0 if last_week_icome is None else round(last_week_icome, 2)
        context['last_week_days'] = last_week_days
        context['last_week_income_chart'] = last_week_income_chart
        context['total_users'] = total_users
        context['total_orders'] = orders_current_week.count()
        context['total_order_progress'] = 0 if orders_progress is None else round(orders_progress, 2)
        context['notify_me_percent'] = int((user_notified / total_users) * 100)
        context['total_income'] = 0 if income_current_week is None else round(income_current_week, 2)
        context['total_income_progress'] = 0 if income_progress is None else round(income_progress, 2)
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
def http_exceptions_handler(request: HttpRequest, exc: ValidationError) \
        -> HttpResponse:
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
            "error": {"status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                      "details": error_list},
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
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
