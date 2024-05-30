import requests
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta

def get_crypto_prices(request):
    try:
        # Get current prices
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd')
        current_prices = response.json()

        # Get prices 24 hours ago
        yesterday = datetime.now() - timedelta(days=1)
        timestamp = int(yesterday.timestamp())
        
        # Fetch BTC price 24 hours ago
        btc_response = requests.get(f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={timestamp}&to={timestamp}')
        btc_prices = btc_response.json()
        if 'prices' in btc_prices and len(btc_prices['prices']) > 0:
            btc_price_yesterday = btc_prices['prices'][0][1]
        else:
            btc_price_yesterday = current_prices['bitcoin']['usd']

        # Fetch ETH price 24 hours ago
        eth_response = requests.get(f'https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=usd&from={timestamp}&to={timestamp}')
        eth_prices = eth_response.json()
        if 'prices' in eth_prices and len(eth_prices['prices']) > 0:
            eth_price_yesterday = eth_prices['prices'][0][1]
        else:
            eth_price_yesterday = current_prices['ethereum']['usd']

        # Calculate the percentage change
        btc_change = (current_prices['bitcoin']['usd'] - btc_price_yesterday) / btc_price_yesterday * 100
        eth_change = (current_prices['ethereum']['usd'] - eth_price_yesterday) / eth_price_yesterday * 100

        data = {
            'BTC': {
                'current_price': current_prices['bitcoin']['usd'],
                'change_percent': btc_change
            },
            'ETH': {
                'current_price': current_prices['ethereum']['usd'],
                'change_percent': eth_change
            }
        }
    except Exception as e:
        data = {'error': str(e)}

    return JsonResponse(data)

def home(request):
    return render(request, 'prices/home.html')
