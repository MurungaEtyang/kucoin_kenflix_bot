import time
from datetime import datetime
import kucoin.client as kc
from kucoin.client import KucoinAPIException

class CoinTrader:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.client = kc.Client(api_key, api_secret, api_passphrase)

    def execute_operations(self, symbol_lists, amounts_usdt, sell_percentages, buy_time):
        # Convert buy_time list to datetime object
        buy_datetime = datetime(*buy_time)

        # Wait until the specified buy time
        self.wait_until_buy_time(buy_datetime)

        # Buy the coins for each set of symbols
        for symbols, amount_usdt, sell_percentage in zip(symbol_lists, amounts_usdt, sell_percentages):
            # Ensure the order amount meets the minimum requirement
            if amount_usdt < 0.1:
                print("Order amount must be at least 0.1 USDT. Skipping this set of symbols.")
                continue

            # Buy the coins and store the buy prices
            buy_prices = []
            bought_coins = []
            for symbol in symbols:
                try:
                    # Get the current market price for the symbol
                    current_price = float(self.client.get_ticker(symbol)['price'])

                    # Place a limit order to buy the coins at the current market price
                    order = self.client.create_limit_order(symbol, 'buy', price=current_price, size=amount_usdt)

                    # Check if order creation was successful
                    if 'orderId' in order:
                        print(f"Placed limit order to buy {amount_usdt} USDT of {symbol} at {current_price}")
                        buy_prices.append(current_price)
                        break
                    else:
                        print(f"Order creation for {amount_usdt} USDT of {symbol} failed.")
                        print(f"Order response: {order}")
                        continue

                except Exception as e:
                    print(f"Error occurred during order creation for {amount_usdt} USDT of {symbol}: {e}")
                    break

            # If no coins were bought successfully, skip to the next set of symbols
            if not buy_prices:
                print("No coins were bought successfully. Skipping this set of symbols.")
                continue

            print("Waiting for 1 minute after buying the coins...")
            time.sleep(10)

            # Continuously check the prices and sell when they increase by the specified percentage
            while True:
                for i, symbol in enumerate(symbols):
                    # Get the current market price for the symbol
                    current_price = float(self.client.get_ticker(symbol)['price'])

                    # Check if the buy price exists for the current symbol
                    if i < len(buy_prices):
                        buy_price = buy_prices[i]

                        # Calculate the percentage increase
                        percentage_increase = ((current_price - buy_price) / buy_price)


                        if percentage_increase >= sell_percentage:

                            account_balance = float(self.client.get_account_list(symbol=symbol)[0]['balance'])
                            if account_balance >= amount_usdt:
                                # Place a market order to sell the coins
                                order = self.client.create_market_order(symbol, 'sell', size=amount_usdt)

                                print(f"Sold {amount_usdt} USDT of {symbol} at {current_price} increase percentage {percentage_increase}%")

                                # Update the buy price to the current price to prevent selling again
                                buy_prices[i] = current_price
                            else:
                                print(f"Insufficient balance to sell {amount_usdt} USDT of {symbol}. Skipping sell order.")
                        else:
                            print(f"Selling percentage for {symbol} has not been reached.")

                    else:
                        print("Buy price does not exist for the current symbol.")

                # Sleep for a certain interval before checking the prices again (e.g., every 5 minutes)
                time.sleep(3)


    def wait_until_buy_time(self, buy_time):
        current_time = datetime.now()
        time_difference = (buy_time - current_time).total_seconds()
        if time_difference > 0:
            print(f"Waiting for {time_difference} seconds until buy time...")
            time.sleep(time_difference)

# # Initialize the CoinTrader class
# api_key = "65f4b5d6bd5c480001a5265a"
# api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
# api_passphrase = "Evans1324$M"
# coin_trader = CoinTrader(api_key, api_secret, api_passphrase)

# # Define the lists of symbol lists, amounts, sell percentages, and buy time
# symbol_lists = [['XRP-USDT', 'LTC-USDT'], ['BTC-USDT', 'ETH-USDT']]
# amounts = [100, 100]
# sell_percentages = [0.5, 0.5]
# buy_time = [2024, 4, 3, 19, 51, 00]

# # Execute operations for each set of symbols
# coin_trader.execute_operations(symbol_lists, amounts, sell_percentages, buy_time)
