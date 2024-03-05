"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from config import settings
from src.games.api import GamesController
from src.main.api import MainController
from src.users.api import UsersController, AuthController
from src.website.api import api
from src.products.api import ProductController

main_api = NinjaExtraAPI()
# main_api.add_router('', api)
main_api.register_controllers(NinjaJWTDefaultController)

main_api.register_controllers(ProductController)
main_api.register_controllers(UsersController)
main_api.register_controllers(AuthController)
main_api.register_controllers(GamesController)
main_api.register_controllers(MainController)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', main_api.urls),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
