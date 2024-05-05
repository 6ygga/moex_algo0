import datetime as dt

from moexalgo import Ticker
from indicator.Value import Value
import pandas as pd


class Psymbol:
    historical_data = []
    alert = False
    signals = []  # list of required signal instances

    def __init__(self,
                 name,  # ticker name
                 signal_names=['VALUE', ],  # список сигналов которые будем использовать для этой бумаги
                 historical_data_len=100
                 ):
        self.name = name
        self.ticker = Ticker(self.name)
        self.signal_names = signal_names
        self.historical_data_len = historical_data_len
        self.signals = []

        start_date = dt.datetime.now().date() - dt.timedelta(days=historical_data_len)
        end_date = dt.datetime.now().date()
        # self.historical_data = self.ticker.candles(start=start_date, end=end_date)
        self.historical_data = self.ticker.tradestats(start=start_date, end=end_date)

        # инициализируем сигналы из списка
        for signal in signal_names:
            match signal:
                case 'VALUE':
                    self.signals.append(Value())
                case _:
                    raise Exception('Signal name not found')

    def update(self):
        # new_data = self.ticker.candles(start=dt.datetime.now().date() - dt.timedelta(days=3),
        #                                   end=dt.datetime.now().date(),
        #                                   latest=True)
        new_data = self.ticker.tradestats(start=dt.datetime.now().date() - dt.timedelta(days=3),
                                          end=dt.datetime.now().date() - dt.timedelta(days=3),
                                          latest=True)
        if not len(new_data):
            return []

        signal_messages = []

        # прогон новых данных по всем сигналам и собираем сообщения
        for signal in self.signals:
            signal_message = signal.new_data(new_data=new_data, historical_data=self.historical_data)
            if signal_message:
                signal_messages.append(self.name + signal_message)

        self.historical_data = pd.concat([self.historical_data[1:], new_data],
                                         ignore_index=True)  # добавляем новые данные удаляем первый элемент чтобы не увеличивать размер

        return signal_messages
