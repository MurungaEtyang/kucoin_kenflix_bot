import time
from datetime import datetime
import kucoin.client as kc
from kucoin.client import KucoinAPIException

class CoinTrader:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.client = kc.Client(api_key, api_secret, api_passphrase)

    def execute_operations(self, symbol_lists, amounts_usdt, sell_percentages, buy_time):
        buy_datetime = datetime(*buy_time)
        self.wait_until_buy_time(buy_datetime)
        results = []
        for symbols, amount_usdt, sell_percentage in zip(symbol_lists, amounts_usdt, sell_percentages):
            if amount_usdt < 0.1:
                results.append("Order amount must be at least 0.1 USDT. Skipping this set of symbols.")
                continue
            buy_prices = []
            for symbol in symbols:
                try:
                    current_price = float(self.client.get_ticker(symbol)['price'])
                    symbols = self.client.get_symbols()
                    symbol_info = next(s for s in symbols if s['symbol'] == symbol)

                    # min_order_size = float(symbol_info['baseMinSize'])
                    # results.append(f"minimum order: {min_order_size}")

                    # Round the quantity to 1 decimal place and ensure it meets the minimum order size
                    quantity = round(amount_usdt / current_price, 4)
                    results.append(f"Quantity: {quantity}")

                    order = self.client.create_market_order(symbol, 'buy',  size=quantity)
                    if 'orderId' in order:
                        results.append(f"Placed limit order to buy {amount_usdt} USDT of {symbol} at {current_price}")
                        buy_prices.append(current_price)
                        break
                    else:
                        results.append(f"Order creation for {amount_usdt} USDT of {symbol} failed.")
                        results.append(f"Order response: {order}")
                        continue

                except KucoinAPIException as e:
                    results.append(f"Error occurred during order creation for {amount_usdt} USDT of {symbol}: {e}")
                    break
            if not buy_prices:
                results.append("No coins were bought successfully. Skipping this set of symbols.")
                continue

            results.append("Waiting for 1 minute after buying the coins...")
            time.sleep(1)
            while True:
                for i, symbol in enumerate(symbols):
                    current_price = float(self.client.get_ticker(symbol)['price'])
                    if i < len(buy_prices):
                        buy_price = buy_prices[i]
                        percentage_increase = ((current_price - buy_price) / buy_price)
                        if percentage_increase >= sell_percentage:

                            account_balance = float(self.client.get_account_list(symbol=symbol)[0]['balance'])
                            if account_balance >= amount_usdt:
                                order = self.client.create_market_order(symbol, 'sell', size=amount_usdt)

                                if 'orderId' in order:
                                    results.append(f"Placed limit order to buy {amount_usdt} USDT of {symbol} at {current_price}")
                                    buy_prices.append(current_price)
                                    break
                                else:
                                    results.append(f"Order creation for {amount_usdt} USDT of {symbol} failed.")
                                    results.append(f"Order response: {order}")
                                    continue
                                results.append(f"Sold {amount_usdt} USDT of {symbol} at {current_price} increase percentage {percentage_increase}%")
                                buy_prices[i] = current_price
                            else:
                                results.append(f"Insufficient balance to sell {amount_usdt} USDT of {symbol}. Skipping sell order.")
                        else:
                            results.append(f"Selling percentage for {symbol} has not been reached.")

                    else:
                        results.append("Buy price does not exist for the current symbol.")
                # time.sleep(3)
        return results

    def wait_until_buy_time(self, buy_time):
        current_time = datetime.now()
        time_difference = (buy_time - current_time).total_seconds()
        if time_difference > 0:
            return f"Waiting for {time_difference} seconds until buy time..."
            time.sleep(time_difference)

# Initialize the CoinTrader class
# api_key = "65f4b5d6bd5c480001a5265a"
# api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
# api_passphrase = "Evans1324$M"
# coin_trader = CoinTrader(api_key, api_secret, api_passphrase)
#
# # Define the lists of symbol lists, amounts, sell percentages, and buy time
# symbol_lists = [['XRP-USDT', 'LTC-USDT'], ['BTC-USDT', 'ETH-USDT']]
# amounts = [100, 100]
# sell_percentages = [0.5, 0.5]
# buy_time = [2024, 4, 3, 19, 51, 00]
#
# # Execute operations for each set of symbols
# results = coin_trader.execute_operations(symbol_lists, amounts, sell_percentages, buy_time)
# for result in results:
#     print(result)
