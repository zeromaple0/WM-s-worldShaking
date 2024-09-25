from django.urls import path

from . import views

urlpatterns = [
    path("/api", views.api, name="api"),
    path('/getprimeprice', views.getprimeprice, name="getprimeprice"),
    path('/getrivenprice', views.getrivenprice, name="getrivenprice"),
    path('/update_prime_price', views.update_prime_price, name="update_prime_price"),
    path('/update_riven_price', views.update_riven_price, name="update_riven_price"),
    path('/login2wm', views.login2wm, name="login2wm"),
    path('/getmessage', views.getmessage, name="getmessage"),
]
