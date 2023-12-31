"""
URL configuration for mercadona project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from promotionApp.views import ProductList
from promotionApp.views import CategoryList
from promotionApp.views import PromotionList
from promotionApp.views import redirect_to_admin

urlpatterns = [
    path('', redirect_to_admin, name='redirect_to_admin'),
    path('admin/', admin.site.urls),
    path('api/products/', ProductList.as_view(), name='product-list'),
    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/promotions/', PromotionList.as_view(), name='promotion-list'),
]