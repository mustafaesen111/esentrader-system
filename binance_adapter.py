# binance_adapter.py
import requests
import time
import hmac
import hashlib

class BinanceBroker:
    def __init__(self, key, secret):
        self.API_KEY = key
        self.API_SECRET = secret
        self.BASE_URL = 'https://api.binance.com'
        self.headers = {"X-MBX-APIKEY": self.API_KEY}

    def _sign(self, params):
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(self.API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params['signature'] = signature
        return params

    def get_account_info(self):
        params = {'timestamp': int(time.time() * 1000)}
        signed_params = self._sign(params)
        url = self.BASE_URL + '/api/v3/account'
        response = requests.get(url, headers=self.headers, params=signed_params)
        return response.json()

    def get_price(self, symbol):
        url = self.BASE_URL + '/api/v3/ticker/price'
        response = requests.get(url, params={"symbol": symbol})
        return float(response.json()['price'])

    def place_order(self, symbol, side, quantity):
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity,
            'timestamp': int(time.time() * 1000)
        }
        signed_params = self._sign(params)
        url = self.BASE_URL + '/api/v3/order'
        response = requests.post(url, headers=self.headers, params=signed_params)
        return response.json()
