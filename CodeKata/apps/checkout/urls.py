from django.urls import path
from . import views

urlpatterns = [
    path("checkout_cart/", views.checkout_cart)
    ]
