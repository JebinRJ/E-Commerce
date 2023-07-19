"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('collections', views.collections, name='collections'),
    path('cart/', views.cart_page, name='cart'),
    path('collections/<str:name>', views.collectionsview, name='collectionsview'),
    path('collections/<str:cname>/<str:pname>',
         views.product_details, name='productview'),
    path('addcart', views.add_to_cart, name='addcart'),
    path('fav', views.fav, name='fav'),
    path('favviewpage', views.favviewpage, name='favviewpage'),
    path('remove_fav/<str:fid>', views.remove_fav, name='remove_fav'),
    path('remove_cart/<str:cid>', views.remove_cart, name='remove_cart'),



]
