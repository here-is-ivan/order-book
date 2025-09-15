import requests

BTC_AMOUNT = 10

COINBASE_API_URL = 'https://api.exchange.coinbase.com/products/BTC-USD/book?level=2'
COINBASE_RESPONSE = requests.get(COINBASE_API_URL)

if COINBASE_RESPONSE.status_code == 200:
    COINBASE_DATA = COINBASE_RESPONSE.json()

    bids = [[float(price), float(size)] for price, size, _ in COINBASE_DATA['bids']]
    asks = [[float(price), float(size)] for price, size, _ in COINBASE_DATA['asks']]

    remaining = BTC_AMOUNT
    sell_revenue = 0

    for price, size in bids:
        if remaining <= 0:
            break
        take = min(size, remaining)
        sell_revenue += take * price
        remaining -= take

    remaining = BTC_AMOUNT
    buy_cost = 0

    for price, size in asks:
        if remaining <= 0:
            break
        take = min(size, remaining)
        buy_cost += take * price
        remaining -= take

    print(f'To buy {BTC_AMOUNT} BTC: ${buy_cost}')
    print(f'To sell {BTC_AMOUNT} BTC: ${sell_revenue}')