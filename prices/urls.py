from django.urls import path
from .views import get_crypto_prices, home

urlpatterns = [
    path('', home),
    path('crypto-prices/', get_crypto_prices),
]
