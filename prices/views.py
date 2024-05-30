import requests
from django.http import JsonResponse
from django.shortcuts import render

def get_crypto_prices(request):
    try:
        # Get current prices and price changes
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets', params={
            'vs_currency': 'usd',
            'ids': 'bitcoin,ethereum,avalanche-2',
            'order': 'market_cap_desc',
            'per_page': 3,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '1h,24h,7d'
        })
        prices = response.json()

        data = {
            'BTC': {
                'current_price': prices[0]['current_price'],
                'change_1h': prices[0]['price_change_percentage_1h_in_currency'],
                'change_24h': prices[0]['price_change_percentage_24h_in_currency'],
                'change_7d': prices[0]['price_change_percentage_7d_in_currency'],
                'alert_1h': abs(prices[0]['price_change_percentage_1h_in_currency']) >= 5,
                'alert_24h': abs(prices[0]['price_change_percentage_24h_in_currency']) >= 5,
                'alert_7d': abs(prices[0]['price_change_percentage_7d_in_currency']) >= 5
            },
            'ETH': {
                'current_price': prices[1]['current_price'],
                'change_1h': prices[1]['price_change_percentage_1h_in_currency'],
                'change_24h': prices[1]['price_change_percentage_24h_in_currency'],
                'change_7d': prices[1]['price_change_percentage_7d_in_currency'],
                'alert_1h': abs(prices[1]['price_change_percentage_1h_in_currency']) >= 5,
                'alert_24h': abs(prices[1]['price_change_percentage_24h_in_currency']) >= 5,
                'alert_7d': abs(prices[1]['price_change_percentage_7d_in_currency']) >= 5
            },
            'AVAX': {
                'current_price': prices[2]['current_price'],
                'change_1h': prices[2]['price_change_percentage_1h_in_currency'],
                'change_24h': prices[2]['price_change_percentage_24h_in_currency'],
                'change_7d': prices[2]['price_change_percentage_7d_in_currency'],
                'alert_1h': abs(prices[2]['price_change_percentage_1h_in_currency']) >= 5,
                'alert_24h': abs(prices[2]['price_change_percentage_24h_in_currency']) >= 5,
                'alert_7d': abs(prices[2]['price_change_percentage_7d_in_currency']) >= 5
            }
        }
    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)

def home(request):
    return render(request, 'prices/home.html')
