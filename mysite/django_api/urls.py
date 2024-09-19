from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('/getprimeprice', views.getprimeprice, name="getprimeprice"),
    path('/getrivenprice', views.getrivenprice, name="getrivenprice"),
    path('/update_prime_price', views.update_prime_price, name="update_prime_price"),
]
