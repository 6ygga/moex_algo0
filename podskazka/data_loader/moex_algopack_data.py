from datetime import datetime, timedelta
import json
import pandas as pd
from moexalgo import Ticker


class MoexAlgopackData:
    historical_data_len = 100
    historical_data = pd.DataFrame()
    last_tradeno = 0

    def __init__(self, ticker_name:str):
        self.ticker_name = ticker_name
        self.ticker = Ticker(self.ticker_name)
        self.update_data()

    def update_data(self):
        # new_data = self.ticker.candles(start=dt.datetime.now().date() - dt.timedelta(days=3),
        #                                   end=dt.datetime.now().date(),
        #                                   latest=True)

        # start_date = dt.datetime.now().date() - dt.timedelta(days=historical_data_len)
        # end_date = dt.datetime.now().date()
        # self.historical_data = self.ticker.candles(start=start_date, end=end_date)  # данные о свечах (малое количество данных поэтому не используется)
        # self.historical_data = self.ticker.tradestats(start=start_date, end=end_date)  # новые расширенные данные по свечам

        new_data = self.ticker.tradestats(start=datetime.now().date(),
                                          end=datetime.now().date(),
                                          latest=True)
        self.historical_data = pd.concat([self.historical_data[1:], new_data],
                                         ignore_index=True)  # добавляем новые данные удаляем первый элемент чтобы не увеличивать размер

        if not len(new_data):
                return []
