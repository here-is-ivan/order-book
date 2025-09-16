import argparse
import requests

COINBASE_API_URL = 'https://api.exchange.coinbase.com/products/BTC-USD/book?level=2'
GEMINI_API_URL = 'https://api.gemini.com/v1/book/BTCUSD'

def fetch_coinbase():
    response = requests.get(COINBASE_API_URL)
    response.raise_for_status()
    data = response.json()
    bids = [[float(price), float(size)] for price, size, _ in data["bids"]]
    asks = [[float(price), float(size)] for price, size, _ in data["asks"]]
    return bids, asks

def fetch_gemini():
    response = requests.get(GEMINI_API_URL)
    response.raise_for_status()
    data = response.json()
    bids = [[float(bid["price"]), float(bid["amount"])] for bid in data["bids"]]
    asks = [[float(ask["price"]), float(ask["amount"])] for ask in data["asks"]]
    return bids, asks

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
        msg = "Not enough asks to buy" if side == "buy" else "Not enough bids to sell"
        raise ValueError(msg)

    return total

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qty", type=float, default=10.0)
    btc_amount = parser.parse_args().qty

    coinbase_bids, coinbase_asks = fetch_coinbase()
    gemini_bids, gemini_asks = fetch_gemini()

    bids = merge_sorted(coinbase_bids, gemini_bids, reverse=True)
    asks = merge_sorted(coinbase_asks, gemini_asks, reverse=False)

    buy_cost = execute(asks, btc_amount, "buy")
    sell_revenue = execute(bids, btc_amount, "sell")

    print(f"To buy {btc_amount} BTC: ${buy_cost:,.2f}")
    print(f"To sell {btc_amount} BTC: ${sell_revenue:,.2f}")

if __name__ == "__main__":
    main()