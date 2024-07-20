from datetime import datetime, timedelta
from .moex_utils import *
import json
import pandas as pd


class MoexTickData:
    historical_data:pd.DataFrame = None
    last_tradeno = 10668474414

    def __init__(self, ticker_name:str):
        self.ticker_name = ticker_name
        self.update_data()

    def update_data(self):
        new_data = get_all_trades(self.ticker_name, start_tradeno=self.last_tradeno)

        if not self.historical_data:
            self.historical_data = new_data
        else:
            self.historical_data = pd.concat([self.historical_data, new_data]).tail(10100)

        self.last_tradeno = new_data['TRADENO'].iloc[-1]

    def get_last_N_sec(self, n=5):
        self.historical_data['TRADETIME'] = pd.to_timedelta(self.historical_data['TRADETIME'])
        # Get the current time and convert to timedelta since start of the day
        now = datetime.now().time()
        # now = datetime.fromisoformat('2024-05-24 20:37:54')
        current_time = pd.to_timedelta(now.strftime('%H:%M:%S'))

        # Calculate the threshold for the last 5 seconds
        threshold = current_time - pd.Timedelta(seconds=n)

        # Filter rows within the last 5 seconds
        last_N_seconds = self.historical_data[self.historical_data['TRADETIME'] > threshold]
        last_N_seconds.reset_index(inplace=True)

        return last_N_seconds

    def tick_value_middle(self):
        f = open('./data_loader.json', 'r')
        data = json.load(f)
        return data['middle_tick_value'][self.ticker_name]

