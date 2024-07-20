# import numpy as np


# Сигнал Аномального объема (Value) на тиках
class ValueTicks:
    value = 0
    name = 'Extra Trade Value'
    history = []

    def __init__(self, data):
        self.data = data

    def new_data(self):
        self.data.update_data()
        print(self.data.historical_data)
        print(f'{self.data.l:.2f}/{self.middle:.2f} {self.name}')
        if self.value > self.data.tick_value_middle() * 5:
            return f'Аномальный объем {self.value:.2f}/{self.middle:.2f}'  # Сообщение от Сигнала Аномального объема

        return ''
