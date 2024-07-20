import numpy as np

from podskazka.data_loader.moex_algopack_data import MoexAlgopackData


# Сигнал Аномального объема (Value) на пятиминутках
class Value:
    value = 0
    name = 'Extra Value'
    history = []
    middle = 0

    def __init__(self, data:MoexAlgopackData):
        self.data = data

    def new_data(self): # надо переделать получение данных
        self.data.update_data()
        # self.middle = np.mean(historical_data['val'])
        # self.middle = np.mean(historical_data['value'])
        # self.value = new_data['val'][0]

        print(f'{self.value:.2f}/{self.middle:.2f} {self.name}')
        if self.value > self.middle * 5:
            return f'Аномальный объем {self.value:.2f}/{self.middle:.2f}'  # Сообщение от Сигнала Аномального объема

        return ''

