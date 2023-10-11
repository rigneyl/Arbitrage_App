import requests

def get_all_pairs_binance():
    binance_url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(binance_url)
    data = response.json()
    pairs = {symbol['symbol']: symbol['baseAsset'] + '-' + symbol['quoteAsset'] for symbol in data['symbols']}
    return pairs

def get_all_pairs_coinbase():
    coinbase_url = 'https://api.pro.coinbase.com/products'
    response = requests.get(coinbase_url)
    data = response.json()
    pairs = {item['id']: item['id'] for item in data}
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
    pairs_binance = get_all_pairs_binance()
    pairs_coinbase = get_all_pairs_coinbase()
    
    common_pairs = set(pairs_binance.values()).intersection(pairs_coinbase.values())
    
    opportunities = []
    
    for pair in common_pairs:
        pair_binance = [k for k, v in pairs_binance.items() if v == pair][0]
        pair_coinbase = [k for k, v in pairs_coinbase.items() if v == pair][0]
        
        price_binance = get_price_binance(pair_binance)
        price_coinbase = get_price_coinbase(pair_coinbase)
        
        if price_binance is None or price_coinbase is None:
            print(f"Skipping {pair} due to error fetching price.")
            continue
        
        if price_binance < price_coinbase:
            opportunities.append(f'Arbitrage Opportunity for {pair}: Buy on Binance at ${price_binance}, Sell on Coinbase Pro at ${price_coinbase}')
        elif price_coinbase < price_binance:
            opportunities.append(f'Arbitrage Opportunity for {pair}: Buy on Coinbase Pro at ${price_coinbase}, Sell on Binance at ${price_binance}')
        else:
            opportunities.append(f'No arbitrage opportunity for {pair}')
    
    return opportunities

