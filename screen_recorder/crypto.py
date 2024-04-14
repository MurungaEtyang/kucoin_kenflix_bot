import base64
import hashlib
import hmac
import time
import requests
import json

class KucoinAPI:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase

    def _generate_signature(self, method, endpoint, timestamp):
        str_to_sign = str(timestamp) + method + endpoint
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            str_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature)

    def _generate_passphrase(self):
        return base64.b64encode(self.api_passphrase.encode('utf-8'))

    def get_ticker_data(self, url):
        now = int(time.time() * 1000)
        headers = {
            "KC-API-SIGN": self._generate_signature('GET', '/api/v1/market/allTickers', now),
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self._generate_passphrase(),
            "KC-API-KEY-VERSION": "2"
        }
        response = requests.get(url, headers=headers)
        return response.json()

def fetch_ticker_data_from_database(database_name='ticker_data.json'):
    try:
        with open(database_name, 'r') as json_file:
            fetched_data = json.load(json_file)
        return fetched_data
    except Exception as e:
        print(f"Error occurred while fetching data from database {database_name}: {e}")
        return None

def save_ticker_data_to_json(api_key, api_secret, api_passphrase, url, database_name='ticker_data.json'):
    api = KucoinAPI(api_key, api_secret, api_passphrase)

    # Fetch ticker data from Kucoin API
    response_data = api.get_ticker_data(url)

    if 'data' in response_data and 'ticker' in response_data['data']:
        ticker_data = response_data['data']['ticker']

        data_to_write = []
        volume_differences = {}  # Dictionary to store volume differences

        # Fetch data from the saved file (database)
        fetched_data = fetch_ticker_data_from_database(database_name)

        if fetched_data:
            print("\nVolume Difference (Percentage):")
            for item_new in ticker_data:
                symbol_new = item_new['symbol']
                volume_new = float(item_new['vol'])

                for item_old in fetched_data:
                    symbol_old = item_old['Symbol']
                    volume_old = float(item_old['Volume'])

                    if symbol_new == symbol_old:
                        volume_difference = ((volume_new - volume_old) / volume_old) * 100
                        volume_differences[symbol_new] = volume_difference
                        print(f"{symbol_new}: {volume_difference:.2f}%")
                        break
        else:
            print(f"Failed to fetch data from the database {database_name}.")

        for item in ticker_data:
            data_to_write.append({
                "Symbol": item.get('symbol'),
                "Buy": item.get('buy'),
                "Sell": item.get('sell'),
                "Change Rate": item.get('changeRate'),
                "Change Price": item.get('changePrice'),
                "High": item.get('high'),
                "Low": item.get('low'),
                "Volume": float(item.get('vol')),  # Convert to float
                "Volume Value": item.get('volValue')
            })

        try:
            with open(database_name, 'w') as json_file:
                json.dump(data_to_write, json_file, indent=4)
            print(f"Data has been written to {database_name}")
        except Exception as e:
            print(f"Error occurred while writing to file {database_name}: {e}")

        return volume_differences

    else:
        print("No ticker data found in the response.")

# Function to fetch ticker data from the KuCoin API and save it to a JSON file
def fetch_and_save(api_key, api_secret, api_passphrase, url, database_name):
    # Delay based on the database name
    if database_name == 'ticker_data_1.json':
        time.sleep(5)
    elif database_name == 'ticker_data_2.json':
        time.sleep(30)
    elif database_name == 'ticker_data_3.json':
        time.sleep(2 * 60)
    elif database_name == 'ticker_data_4.json':
        time.sleep(5 * 60)
    elif database_name == 'ticker_data_5.json':
        time.sleep(10 * 60)
    elif database_name == 'ticker_data_6.json':
        time.sleep(15 * 60)

    # Call the function to save ticker data to JSON
    save_ticker_data_to_json(api_key, api_secret, api_passphrase, url, database_name)

# Example usage:
if __name__ == "__main__":
    api_key = "65f4b5d6bd5c480001a5265a"
    api_secret = "cd7fde2b-3b38-4f98-8ca1-12a48d0f7af5"
    api_passphrase = "Evans1324$M"
    url = 'https://api.kucoin.com/api/v1/market/allTickers'

    # List of database names
    databases = ['ticker_data_1.json', 'ticker_data_2.json', 'ticker_data_3.json',
                 'ticker_data_4.json', 'ticker_data_5.json', 'ticker_data_6.json']

    for db_name in databases:
        fetch_and_save(api_key, api_secret, api_passphrase, url, db_name)
