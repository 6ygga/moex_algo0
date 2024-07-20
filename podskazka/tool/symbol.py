# from podskazka.data_loader.moex_algopack_data import MoexAlgopackData
# from podskazka.signal.Value import Value

from .moex_tick_data import MoexTickData
from .Value_ticks import ValueTicks


class Psymbol:
    historical_data = []
    alert = False
    signals = []  # list of required signal instances

    def __init__(self,
                 ticker_name,  # ticker name
                 signal_names=None,  # список сигналов которые будем использовать для этой бумаги
                 ):

        if signal_names is None:
            signal_names = ['VALUE_TICK', ]

        self.ticker_name = ticker_name
        self.signal_names = signal_names
        self.signals = []

        # инициализируем сигналы из списка
        for signal in signal_names:
            match signal:
                # case 'VALUE':
                #     self.signals.append(Value(MoexAlgopackData(ticker_name=self.ticker_name)))
                case 'VALUE_TICK':
                    self.signals.append(ValueTicks(MoexTickData(ticker_name=self.ticker_name)))
                case _:
                    raise Exception('Signal name not found')

    def update(self):
        signal_messages = []

        # прогон новых данных по всем сигналам и собираем сообщения
        for signal in self.signals:
            signal_message = signal.new_data()
            if signal_message:
                signal_messages.append(f'{self.name} {signal_message}')

        return signal_messages
