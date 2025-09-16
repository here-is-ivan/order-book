import requests

BTC_AMOUNT = 10

COINBASE_API_URL = 'https://api.exchange.coinbase.com/products/BTC-USD/book?level=2'
COINBASE_RESPONSE = requests.get(COINBASE_API_URL)

GEMINI_API_URL = 'https://api.gemini.com/v1/book/BTCUSD'
GEMINI_RESPONSE = requests.get(GEMINI_API_URL)

if COINBASE_RESPONSE.status_code == 200 and GEMINI_RESPONSE.status_code == 200:
    COINBASE_DATA = COINBASE_RESPONSE.json()
    GEMINI_DATA = GEMINI_RESPONSE.json()

    coinbase_bids = [[float(p), float(s)] for p, s, _ in COINBASE_DATA["bids"]]
    coinbase_asks = [[float(p), float(s)] for p, s, _ in COINBASE_DATA["asks"]]
    gemini_bids = [[float(b["price"]), float(b["amount"])] for b in GEMINI_DATA["bids"]]
    gemini_asks = [[float(a["price"]), float(a["amount"])] for a in GEMINI_DATA["asks"]]


    def merge_sorted(a, b, reverse=False):
        i = j = 0
        merged = []

        while i < len(a) and j < len(b):
            if (a[i][0] >= b[j][0]) if reverse else (a[i][0] <= b[j][0]):
                merged.append(a[i])
                i += 1
            else:
                merged.append(b[j])
                j += 1

        merged.extend(a[i:])
        merged.extend(b[j:])
        return merged

    bids = merge_sorted(coinbase_bids, gemini_bids, reverse=True)
    asks = merge_sorted(coinbase_asks, gemini_asks, reverse=False)

    def execute(orderbook, qty, side):
        remaining = qty
        total = 0
        for price, size in orderbook:
            if remaining <= 0:
                break
            take = min(size, remaining)
            total += take * price
            remaining -= take

        if remaining > 0:
            if side == 'buy':
                raise ValueError("Not enough asks to buy")
            elif side == 'sell':
                raise ValueError("Not enough bids to sell")

        return total

    buy_cost = execute(asks, BTC_AMOUNT, 'buy')
    sell_revenue = execute(bids, BTC_AMOUNT, 'sell')

    print(f'To buy {BTC_AMOUNT} BTC: ${buy_cost}')
    print(f'To sell {BTC_AMOUNT} BTC: ${sell_revenue}')