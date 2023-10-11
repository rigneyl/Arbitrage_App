import requests

# Specify the trading pairs of interest
TARGET_PAIRS_BINANCE = {'BTCUSDT', 'ETHUSDT', 'XRPUSDT'}
TARGET_PAIRS_COINBASE = {'BTC-USD', 'ETH-USD', 'XRP-USD'}

# Mapping Binance pairs to Coinbase pairs
PAIRS_MAPPING = {'BTCUSDT': 'BTC-USD', 'ETHUSDT': 'ETH-USD', 'XRPUSDT': 'XRP-USD'}

def get_all_pairs_binance():
    binance_url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(binance_url)
    data = response.json()
    pairs = {symbol['symbol']: symbol['symbol'] 
             for symbol in data['symbols'] if symbol['symbol'] in TARGET_PAIRS_BINANCE}
    return pairs

def get_all_pairs_coinbase():
    coinbase_url = 'https://api.pro.coinbase.com/products'
    response = requests.get(coinbase_url)
    data = response.json()
    pairs = {item['id']: item['id'] 
             for item in data if item['id'] in TARGET_PAIRS_COINBASE}
    return pairs

def get_price_binance(pair):
    binance_url = f'https://api.binance.com/api/v3/ticker/price?symbol={pair}'
    response = requests.get(binance_url)
    data = response.json()
    return float(data['price'])

def get_price_coinbase(pair):
    coinbase_url = f'https://api.pro.coinbase.com/products/{pair}/ticker'
    response = requests.get(coinbase_url)
    data = response.json()
    try:
        return float(data['price'])
    except KeyError:
        print(f"Error retrieving price for {pair} from Coinbase Pro: {data}")
        return None

def find_arbitrage_opportunities():
    # ...
    opportunities = []
    trade_value = 100000  # Define the trade value
    
    for pair_binance, pair_coinbase in PAIRS_MAPPING.items():
        price_binance = get_price_binance(pair_binance)
        price_coinbase = get_price_coinbase(pair_coinbase)
        
        if price_binance is None or price_coinbase is None:
            print(f"Skipping {pair_binance}/{pair_coinbase} due to error fetching price.")
            continue
        
        if price_binance < price_coinbase:
            profit = (price_coinbase - price_binance) * (trade_value / price_binance)
            opportunities.append({
                'message': f'Buy {pair_binance} on Binance at ${price_binance}, Sell {pair_coinbase} on Coinbase Pro at ${price_coinbase}',
                'profit': profit
            })
        elif price_coinbase < price_binance:
            profit = (price_binance - price_coinbase) * (trade_value / price_coinbase)
            opportunities.append({
                'message': f'Buy {pair_coinbase} on Coinbase Pro at ${price_coinbase}, Sell {pair_binance} on Binance at ${price_binance}',
                'profit': profit
            })
        else:
            opportunities.append({
                'message': f'No arbitrage opportunity for {pair_binance}/{pair_coinbase}',
                'profit': 0
            })
    
    return opportunities
