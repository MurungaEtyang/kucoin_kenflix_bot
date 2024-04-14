import json

class DateTime:
    def __init__(self, data):
        self.__dict__.update(data)
    @classmethod
    def from_json_file(cls):
        with open("time_for_purchase.json", 'r') as file:
            json_data = file.read()
        data = json.loads(json_data)
        return cls(data)

    def get_year(self):
        return self.Year
    
    def get_month(self):
        return self.Month
    
    def get_day(self):
        return self.Day
    
    def get_hour(self):
        return self.Hour
    
    def get_minute(self):
        return self.Minute
    
    def get_second(self):
        return self.Second

class Sell:
    def __init__(self, data):
        self.__dict__.update(data)

    @classmethod
    def from_json_file(cls):
        with open("sell_when_price_%_reach.json", 'r') as file:
            json_data = file.read()
        data = json.loads(json_data)
        return cls(data)

    def get_coin1(self):
        return self.Coin1
    
    def get_coin2(self):
        return self.Coin2
    
    def get_coin3(self):
        return self.Coin3
    
    def get_coin4(self):
        return self.Coin4


class Buy:
    def __init__(self, data):
        self.__dict__.update(data)

    @classmethod
    def from_json_file(cls):
        with open("buy_amount.json", 'r') as file:
            json_data = file.read()
        data = json.loads(json_data)
        return cls(data)

    def get_amount_coin1(self):
        return self.Amount1
    
    def get_amount_coin2(self):
        return self.Amount2
    
    def get_amount_coin3(self):
        return self.Amount3
    
    def get_amount_coin4(self):
        return self.Amount4
