from kucoin.client import Client

class CoinMonitor:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.client = Client(api_key, api_secret, api_passphrase)

    def get_price(self, coin):
        try:
            ticker = self.client.get_ticker(symbol=f"{coin}-USDT")
            return float(ticker['price'])
        except Exception as e:
            print(f"An error occurred while fetching the price of {coin}: {e}")
            return None

# if __name__ == "__main__":
    # # Replace these with your actual Kucoin API credentials
    # api_key = "65f4b5d6bd5c480001a5265a"
    # api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
    # api_passphrase = "Evans1324$M"

    # # Create an instance of CoinMonitor
    # coin_monitor = CoinMonitor(api_key, api_secret, api_passphrase)

    # # Create an instance of CoinMonitor
    # coin_monitor = CoinMonitor(api_key, api_secret, api_passphrase)

    # # List of coins to fetch prices for
    # coins_to_check = ["RMRK", "SUKU", "GHX", "SKEY"]

    # # Iterate over the list of coins and fetch their prices
    # for coin_symbol in coins_to_check:
    #     price = coin_monitor.get_price(coin_symbol)
        
    #     if price is not None:
    #         print(f"The current price of {coin_symbol} is: {price} USDT")
    #     else:
    #         print(f"Failed to fetch the price of {coin_symbol}")
