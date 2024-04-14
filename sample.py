import math

import kucoin.client as kc

# Replace these with your own API keys
api_key = "65f4b5d6bd5c480001a5265a"
api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
api_passphrase = "Evans1324$M"
# Initialize the KuCoin client
client = kc.Client(api_key, api_secret, api_passphrase)

# Define the parameters for your buy order
symbol = 'TON-USDT'  # Trading pair
usdt_to_spend = 1  # Amount of USDT you want to spend

# Get the current price of TON
ticker = client.get_ticker(symbol)
ton_price = float(ticker['price'])

# Calculate the quantity of TON you can buy with 1 USDT
quantity = usdt_to_spend / ton_price
print(quantity)
# Get trading symbols to find the minimum order size
symbols = client.get_symbols()

# Find the symbol information for the trading pair
symbol_info = next(s for s in symbols if s['symbol'] == symbol)

# Extract the minimum order size
min_order_size = float(symbol_info['baseMinSize'])

# Round the quantity to 1 decimal place and ensure it meets the minimum order size
quantity = round(quantity / min_order_size, 1) * min_order_size
print(quantity)

# Place a market buy order for TON
order = client.create_market_order(symbol, 'buy', size=quantity)

print(quantity)