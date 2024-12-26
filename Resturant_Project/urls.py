"""
URL configuration for Resturant_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from Base_App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('menu/',menu,name='menu'),
    path('book/',book,name='book'),
    path('about/',about,name='about'),
    path('signup/',signup,name='signup'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('cart/',cart,name='cart'),
    path('add-to-cart/<int:dish_id>',add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>',remove_from_cart,name='remove_from_cart'),
    path('checkout',checkout,name='checkout'),
    path('orders',order_list,name='order_list'),
    path('order/<int:order_id>',order_details,name='order_details')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)