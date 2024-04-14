import json
import sys

import pyttsx3
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer
from crypto import KucoinAPI

class MainWindow(QMainWindow):
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

        self.refresh_button = QPushButton("Refresh Data")
        layout.addWidget(self.refresh_button)

        self.refresh_button.clicked.connect(self.refresh_data)

        self.api_key = "65f4b5d6bd5c480001a5265a"
        self.api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
        self.api_passphrase = "Evans1324$M"
        self.url = 'https://api.kucoin.com/api/v1/market/allTickers'
        self.databases = ['ticker_data_1.json', 'ticker_data_2.json']

        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(4000)  # 10 seconds interval

    def fetch_ticker_data(self):
        api = KucoinAPI(self.api_key, self.api_secret, self.api_passphrase)
        response_data = api.get_ticker_data(self.url)
        return response_data

    def save_ticker_data_to_json(self, database_name):
        api = KucoinAPI(self.api_key, self.api_secret, self.api_passphrase)

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

                    for item_old in fetched_data:
                        symbol_old = item_old['Symbol']
                        volume_old = float(item_old['Volume'])

                        if symbol_new == symbol_old:
                            volume_difference = volume_new - volume_old
                            volume_difference_percentage = ((volume_new - volume_old) / volume_old) * 100 if volume_old != 0 else 0
                            volume_differences[symbol_new] = (volume_difference, volume_difference_percentage)
                            break

            for item in ticker_data:
                data_to_write.append({
                    "Symbol": item.get('symbol'),
                    "Volume": float(item.get('vol'))
                })

            try:
                with open(database_name, 'w') as json_file:
                    json.dump(data_to_write, json_file, indent=4)
            except Exception as e:
                print(f"Error occurred while writing to file {database_name}: {e}")

            return volume_differences

        else:
            print("No ticker data found in the response.")

    def fetch_ticker_data_from_database(self, database_name='ticker_data.json'):
        try:
            with open(database_name, 'r') as json_file:
                fetched_data = json.load(json_file)
            return fetched_data
        except Exception as e:
            print(f"Error occurred while fetching data from database {database_name}: {e}")
            return None

    def refresh_data(self):
        all_volume_differences = {}
        for db_name in self.databases:
            volume_differences = self.save_ticker_data_to_json(db_name)
            if volume_differences:
                all_volume_differences.update(volume_differences)

        # Filter coins that end with "USDT"
        usdt_volume_differences = {symbol: diff for symbol, diff in all_volume_differences.items() if
                                   symbol.endswith('USDT')}

        sorted_volume_differences = dict(
            sorted(usdt_volume_differences.items(), key=lambda item: item[1][1], reverse=True))

        self.table.setRowCount(len(sorted_volume_differences))
        self.table.setColumnCount(len(self.databases) * 2 + 1)
        headers = ["Symbol"] + [f"DB{i + 1} Volume" for i in range(len(self.databases))] + [f"DB{i + 1} % Difference"
                                                                                            for i in
                                                                                            range(len(self.databases))]
        self.table.setHorizontalHeaderLabels(headers)

        row = 0
        for symbol, (volume_difference, volume_difference_percentage) in sorted_volume_differences.items():
            self.table.setItem(row, 0, QTableWidgetItem(symbol))
            for col, db_name in enumerate(self.databases):
                self.table.setItem(row, col * 2 + 1, QTableWidgetItem(str(volume_difference)))
                self.table.setItem(row, col * 2 + 2, QTableWidgetItem(str(volume_difference_percentage)))
                # Check if volume difference percentage is >= 10
                if volume_difference_percentage >= 10:
                    engine = pyttsx3.init()

                    # Adjust properties of the speech
                    engine.setProperty('rate', 150)
                    engine.setProperty('volume', 1.0)

                    # Selecting a female voice
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if "female" in voice.name.lower():
                            engine.setProperty('voice', voice.id)
                            break

                    message = f"{symbol} increased by {volume_difference_percentage:.2f}% in the last {self.timer.interval() / 1000} seconds"
                    engine.say(message)
                    engine.runAndWait()

                    # Change background color of the cell to indicate the coin
                    item = QTableWidgetItem(message)
                    item.setBackground(QColor("yellow"))  # You can change the color as needed
                    self.table.setItem(row, col * 2 + 2, item)
            row += 1

    def auto_refresh(self):
        self.refresh_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
