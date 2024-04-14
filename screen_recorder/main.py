import sys
import requests
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
import random

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

class DataFetcher(QThread):
    data_fetched = pyqtSignal(list)

    def run(self):
        try:
            url = 'https://api.kucoin.com/api/v1/market/allTickers'
            response = requests.get(url)
            if response.status_code == 200:
                ticker_data = response.json()['data']['ticker']
                self.data_fetched.emit(ticker_data)
            else:
                logging.error(f"Failed to fetch ticker data: {response.status_code}")
                self.data_fetched.emit([])
        except Exception as e:
            logging.error(f"An error occurred while fetching data: {e}")
            self.data_fetched.emit([])

class TopGainersWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Top Gainers')
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.coin_status = {}  # Dictionary to store the continuous increase status of each coin
        self.fetch_and_display_top_gainers()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_and_display_top_gainers)
        self.timer.start(1000)  # Refresh every 1 second

    def fetch_and_display_top_gainers(self):
        self.data_fetcher = DataFetcher()
        self.data_fetcher.data_fetched.connect(self.display_top_gainers)
        self.data_fetcher.start()

    def display_top_gainers(self, ticker_data):
        try:
            # Clear existing labels
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().deleteLater()

            top_gainers = sorted(ticker_data, key=lambda x: (float(x['changeRate']), self.coin_status.get(x['symbol'], 0)), reverse=True)[:20]

            for gainer in top_gainers:
                coin_symbol = gainer['symbol']
                change_rate = float(gainer['changeRate'])
                gainer_info = gainer
                info_text = f"vol: {gainer_info['vol']}, buy: {gainer_info['buy']}, sell: {gainer_info['sell']}, changeRate: {gainer_info['changeRate']}"
                prediction = self.predict_next_change(change_rate)
                self.update_continuous_increase_status(coin_symbol, prediction)
                continuous_increase_duration = self.coin_status.get(coin_symbol, 0)
                label_text = f"Coin: {coin_symbol}, Percentage Change: {change_rate:.2f}%, Gainer Info: {info_text}, Continuous Increase Duration: {continuous_increase_duration} seconds"
                label = QLabel(label_text)
                if continuous_increase_duration >= 2:
                    label.setStyleSheet("""
                        background-color: blue;
                        padding: 10px;
                        margin-bottom: 5px;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                    """)
                    label.setText(f"Coin: {coin_symbol}, Percentage Change: {change_rate:.2f}%, Gainer Info: {info_text}, Continuous Increase Duration: {continuous_increase_duration} seconds, 1")
                else:
                    label.setStyleSheet("""
                        background-color: {color};
                        padding: 10px;
                        margin-bottom: 5px;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                    """.format(color="#92d56b" if prediction > 0 else "#ee7688"))  # Green for increase, red for decrease
                self.layout.addWidget(label)
        except Exception as e:
            logging.error(f"An error occurred while displaying data: {e}")

    def predict_next_change(self, current_change_rate):
        return random.uniform(-5, 5)

    def update_continuous_increase_status(self, coin_symbol, prediction):
        if prediction > 0:
            self.coin_status[coin_symbol] = self.coin_status.get(coin_symbol, 0) + 1
        else:
            self.coin_status[coin_symbol] = 0

def main():
    app = QApplication(sys.argv)
    top_gainers_widget = TopGainersWidget()
    top_gainers_widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
