import numpy as np


# Сигнал Аномального объема (Value)
class Value:
    value = 0
    name = 'Extra Value'
    history = []
    middle = 0

    def new_data(self, new_data, historical_data):
        self.middle = np.mean(historical_data['val'])
        # self.middle = np.mean(historical_data['value'])
        self.value = new_data['val'][0]

        print(f'{self.value:.2f}/{self.middle:.2f} {self.name}')
        if self.value > self.middle * 5:
            return f'Аномальный объем {self.value:.2f}/{self.middle:.2f}'  # Сообщение от Сигнала Аномального объема

        return ''

