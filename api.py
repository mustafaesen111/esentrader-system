# api.py
from flask import Flask, request, jsonify
from binance_adapter import BinanceBroker

app = Flask(__name__)

# Senin Binance API keylerin:
API_KEY = "jXCe1KjWHxmGnnhAulfhGlskxxbFJ5XmomQVoiwPI3ISVFM6Hdcg9tMmmlxPMF7I"
API_SECRET = "ZRZgWXIKudai9MOKWn0zIdigdtjBD3WTWg0t8XIDsJ7dzPqN1LQpyzmh0rp83BQc"

broker = BinanceBroker(API_KEY, API_SECRET)

@app.route('/api/account_info')
def account_info():
    return jsonify(broker.get_account_info())

@app.route('/api/price')
def price():
    symbol = request.args.get("symbol", "BTCUSDT")
    return jsonify({"price": broker.get_price(symbol)})

@app.route('/api/order', methods=["POST"])
def order():
    data = request.json
    symbol = data['symbol']
    side = data['side']
    quantity = data['quantity']
    return jsonify(broker.place_order(symbol, side.upper(), quantity))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5060)
