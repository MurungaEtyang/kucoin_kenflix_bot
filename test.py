import json
import os
import sys
import pyttsx3
import requests
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QMessageBox, QTextEdit
from PyQt5.QtCore import QTimer

from data_from_user import DateTime, Sell, Buy

from PyQt5.QtCore import QThread, pyqtSignal

from db import DatabaseManager
from Transact import CoinTrader
from crypto import KucoinAPI


class Secure_word:
    db = DatabaseManager()
    __word = db.fetch_data_kenflix()

    def secure_word(self):
        if self.__word == ["2"]:
            app = QApplication(sys.argv)
            window = MainWindow1()
            window.setGeometry(100, 100, 800, 600)
            window.setWindowTitle("Crypto Trading Inputs")
            window.show()
            sys.exit(app.exec_())

        else:
            data = self.db.fetch_data_message()

            for word in data:
                app = QApplication(sys.argv)
                widget = QWidget()
                QMessageBox.warning(widget, "Security Alert", word)
                sys.exit(app.exec_())

class TradingThread(QThread):
    finished = pyqtSignal()
    results_received = pyqtSignal(str)

    def __init__(self, api_key, api_secret, api_passphrase, coins, buy_price, buy_time, percentage):
        super().__init__()
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.coins = coins
        self.buy_price = buy_price
        self.buy_time = buy_time
        self.percentage = percentage

    def run(self):
        try:
            buy_sale = CoinTrader(self.api_key, self.api_secret, self.api_passphrase)
            results = buy_sale.execute_operations([self.coins], self.buy_price, self.percentage, self.buy_time)
            for result in results:
                self.results_received.emit(result)

        except Exception as e:
            print("An error occurred during trading:", e)
        finally:
            self.finished.emit()


class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KuCoin Ticker Data")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.api_key = "65f4b5d6bd5c480001a5265a"
        self.api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
        self.api_passphrase = "Evans1324$M"
        self.url = "https://api.kucoin.com/api/v1/market/allTickers"
        self.url_orders = "https://api.kucoin.com/api/v1/orders/multi"
        my_db_directory = '/my_db/'
        # Ensure the directory exists, create it if it doesn't
        if not os.path.exists(my_db_directory):
            os.makedirs(my_db_directory)

        self.databases = [os.path.join(my_db_directory, 'ticker_data_1.json')]
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(4000)

        # Add a QTextEdit widget to display results
        self.results_text_edit = QTextEdit()
        self.results_text_edit.setStyleSheet(
            "background-color: #004d99; color: #d9d9d9; font-size: 14px; font-family: Arial;"
        )
        layout.addWidget(self.results_text_edit)

        self.refresh_button = QPushButton("Refresh Data")
        layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.refresh_data)


    def update_results_widget(self, result):
        # Append the received result to the QTextEdit widget
        self.results_text_edit.append(result)

    def check_internet(self):
        try:
            requests.get('http://www.google.com', timeout=1)
            return True
        except requests.ConnectionError:
            return False

    def fetch_ticker_data(self):
        if not self.check_internet():
            QMessageBox.warning(self, "No Internet Connection", "Please check your internet connection.")
            return None

        api = KucoinAPI(self.api_key, self.api_secret, self.api_passphrase)
        try:
            response_data = api.get_ticker_data(self.url)
            if 'data' in response_data and 'ticker' in response_data['data']:
                ticker_data = response_data['data']['ticker']
                for item in ticker_data:
                    symbol = item.get('symbol')
                    price = float(item.get('last'))
                    print(f"Symbol: {symbol}, Price: {price}")
            else:
                print("No ticker data found in the response.")
        except Exception as e:
            print("An error occurred while fetching ticker data:", e)

    def save_ticker_data_to_json(self, database_name):
        api = KucoinAPI(self.api_key, self.api_secret, self.api_passphrase)
        try:
            response_data = api.get_ticker_data(self.url)
            if 'data' in response_data and 'ticker' in response_data['data']:
                ticker_data = response_data['data']['ticker']
                data_to_write = []
                volume_differences = {}
                fetched_data = self.fetch_ticker_data_from_database(database_name)
                if fetched_data:
                    for item_new in ticker_data:
                        symbol_new = item_new['symbol']
                        volume_new = float(item_new['vol'])
                        price_new = float(item_new['last'])
                        for item_old in fetched_data:
                            symbol_old = item_old['Symbol']
                            volume_old = float(item_old['Volume'])
                            if symbol_new == symbol_old:
                                volume_difference = volume_new - volume_old
                                volume_difference_percentage = ((
                                                                        volume_new - volume_old) / volume_old) * 100 if volume_old != 0 else 0
                                volume_differences[symbol_new] = (volume_difference, volume_difference_percentage)
                                break
                for item in ticker_data:
                    data_to_write.append({
                        "Symbol": item.get('symbol'),
                        "Volume": float(item.get('vol')),
                        "Price": float(item.get('last'))
                    })
                with open(database_name, 'w') as json_file:
                    json.dump(data_to_write, json_file, indent=4)
                return volume_differences
            else:
                print("No ticker data fo`und in the response.")
        except Exception as e:
            print(f"An error occurred while saving ticker data to JSON file {database_name}:", e)

    def fetch_ticker_data_from_database(self, database_name='ticker_data_1.json'):
        try:
            with open(database_name, 'r') as json_file:
                fetched_data = json.load(json_file)
            return fetched_data
        except Exception as e:
            print(f"An error occurred while fetching data from database {database_name}: {e}")
            return None

    def refresh_data(self):
        all_volume_differences = {}
        for db_name in self.databases:
            volume_differences = self.save_ticker_data_to_json(db_name)
            if volume_differences:
                all_volume_differences.update(volume_differences)
        sorted_volume_differences = dict(
            sorted(all_volume_differences.items(), key=lambda item: item[1][1], reverse=True))
        filtered_volume_differences = {symbol: (volume_difference, volume_difference_percentage) for
                                       symbol, (volume_difference, volume_difference_percentage) in
                                       sorted_volume_differences.items() if symbol.endswith('-USDT')}
        coin_prices = [(symbol, volume_difference) for symbol, (volume_difference, volume_difference_percentage) in
                       filtered_volume_differences.items()]
        self.table.setRowCount(len(filtered_volume_differences))
        self.table.setColumnCount(len(self.databases) * 2 + 1)
        headers = ["Symbol"] + [f"DB{i + 1} Volume" for i in range(len(self.databases))] + [f"DB{i + 1} % Difference"
                                                                                            for i in
                                                                                            range(len(self.databases))]
        self.table.setHorizontalHeaderLabels(headers)
        row = 0
        for symbol, (volume_difference, volume_difference_percentage) in filtered_volume_differences.items():
            self.table.setItem(row, 0, QTableWidgetItem(symbol))
            for col, db_name in enumerate(self.databases):
                self.table.setItem(row, col * 2 + 1, QTableWidgetItem(str(volume_difference)))
                self.table.setItem(row, col * 2 + 2, QTableWidgetItem(str(volume_difference_percentage)))
                if volume_difference_percentage >= 50:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.setProperty('volume', 1.0)
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[1].id)
                    message = f"{symbol} increased by {volume_difference_percentage:.2f}%"
                    engine.say(message)
                    engine.runAndWait()
                    item = QTableWidgetItem(message)
                    item.setBackground(QColor("yellow"))
                    self.table.setItem(row, col * 2 + 2, item)
            row += 1
        self.print_first_four_coins(coin_prices)

    def print_first_four_coins(self, coin_prices):
        if coin_prices:
            if len(coin_prices) >= 4:
                first_four_coins = coin_prices[:4]
                coins = []
                prices = []
                for coin, price in first_four_coins:
                    coins.append(coin)
                    prices.append(price)
                date_time = DateTime.from_json_file()
                sell_orders = Sell.from_json_file()
                buy_orders = Buy.from_json_file()
                buy_time = [int(date_time.get_year()), int(date_time.get_month()), int(date_time.get_day()),
                            int(date_time.get_hour()), int(date_time.get_minute()), int(date_time.get_second())]
                percentage = [float(sell_orders.get_coin1()), float(sell_orders.get_coin2()),
                              float(sell_orders.get_coin3()), float(sell_orders.get_coin4())]
                buy_price = [float(buy_orders.get_amount_coin1()), float(buy_orders.get_amount_coin2()),
                             float(buy_orders.get_amount_coin3()), float(buy_orders.get_amount_coin4())]
                self.trading_thread = TradingThread(self.api_key, self.api_secret, self.api_passphrase, coins,
                                                    buy_price, buy_time, percentage)

                # Connect the signal to update the results widget
                self.trading_thread.results_received.connect(self.update_results_widget)

                self.trading_thread.finished.connect(self.on_trading_finished)
                self.trading_thread.start()
            else:
                print("Not enough coin prices provided.")
        else:
            print("No coin prices provided.")

    def on_trading_finished(self):
        print("Trading finished.")

    def auto_refresh(self):
        self.refresh_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    word = Secure_word()
    word.secure_word()
    sys.exit(app.exec_())