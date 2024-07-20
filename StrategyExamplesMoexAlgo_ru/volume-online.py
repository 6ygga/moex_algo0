# git clone https://github.com/cia76/AlorPy
# git clone https://github.com/cia76/BackTraderAlor
# pip install

import datetime as dt
import backtrader as bt
from backtrader_moexalgo.moexalgo_store import MoexAlgoStore  # Хранилище AlgoPack

from Config import Config as ConfigMOEX  # для авторизации на Московской Бирже


# Торговая система
class NotifierStrategy(bt.Strategy):
    """
    Демонстрация live стратегии - однократно покупаем по рынку 1 лот и однократно продаем его по рынку через 3 бара
    """
    params = (  # Параметры торговой системы
        ('timeframe', ''),
        ('live_prefix', ''),  # префикс для выставления заявок в live
        ('info_tickers', []),  # информация по тикерам
    )

    def __init__(self):
        """Инициализация, добавление индикаторов для каждого тикера"""
        self.orders = {}  # Организовываем заявки в виде справочника, конкретно для этой стратегии один тикер - одна активная заявка
        for d in self.datas:  # Пробегаемся по всем тикерам
            self.orders[d._name] = None  # Заявки по тикеру пока нет

        # создаем индикаторы для каждого тикера
        self.sma1 = {}
        self.sma2 = {}
        self.rsi = {}
        for i in range(len(self.datas)):
            ticker = list(self.dnames.keys())[i]    # key name is ticker name
            self.sma1[ticker] = bt.indicators.SMA(self.datas[i], period=8)  # SMA indicator
            self.sma2[ticker] = bt.indicators.SMA(self.datas[i], period=16)  # SMA indicator
            self.rsi[ticker] = bt.indicators.RSI(self.datas[i], period=14)  # RSI indicator

        self.buy_once = {}
        self.sell_once = {}

    def start(self):
        for d in self.datas:  # Running through all the tickers
            self.buy_once[d._name] = False
            self.sell_once[d._name] = False

    def next(self):
        """Приход нового бара тикера"""
        for data in self.datas:  # Пробегаемся по всем запрошенным барам всех тикеров
            ticker = data._name
            status = data._state  # 0 - Live data_loader, 1 - History data_loader, 2 - None
            _interval = self.p.timeframe
            _date = bt.num2date(data.datetime[0])

            try:
                if data.p.supercandles[ticker][data.p.metric_name]:
                    # print("\tSuper Candle:", data_loader.p.supercandles[ticker][data_loader.p.metric_name][0])
                    _data = data.p.supercandles[ticker][data.p.metric_name][0]
                    _data['datetime'] = _date
                    self.supercandles[ticker][data.p.metric_name].append(_data)
            except:
                pass

            if status in [0, 1]:
                if status: _state = "False - History data_loader"
                else: _state = "True - Live data_loader"

                if data.tick_volume > 1000000:  # Если есть заявки
                    print('{} / {} [{}] - Open: {}, High: {}, Low: {}, Close: {}, Volume: {} - Live: {}'.format(
                        bt.num2date(data.datetime[0]),
                        data._name,
                        _interval,  # таймфрейм тикера
                        data.open[0],
                        data.high[0],
                        data.low[0],
                        data.close[0],
                        data.volume[0],
                        _state,
                    ))
                    print(f'\t - {ticker} RSI\t\t: {self.rsi[ticker][0]}')

                    print(f"\t - Изменение цены\t: {data.high[0] - data.low[0]}")

                    print(f'\t - Volume\t\t: {data.tick_volume}')

    def notify_order(self, order):
        """Изменение статуса заявки"""
        order_data_name = order.data._name  # Имя тикера из заявки
        print("*"*50)
        self.log(f'Заявка номер {order.ref} {order.info["order_number"]} {order.getstatusname()} {"Покупка" if order.isbuy() else "Продажа"} {order_data_name} {order.size} @ {order.price}')
        if order.status == bt.Order.Completed:  # Если заявка полностью исполнена
            if order.isbuy():  # Заявка на покупку
                self.log(f'Покупка {order_data_name} Цена: {order.executed.price:.2f}, Объём: {order.executed.value:.2f}, Комиссия: {order.executed.comm:.2f}')
            else:  # Заявка на продажу
                self.log(f'Продажа {order_data_name} Цена: {order.executed.price:.2f}, Объём: {order.executed.value:.2f}, Комиссия: {order.executed.comm:.2f}')
                self.orders[order_data_name] = None  # Сбрасываем заявку на вход в позицию
        print("*" * 50)

    def notify_trade(self, trade):
        """Изменение статуса позиции"""
        if trade.isclosed:  # Если позиция закрыта
            self.log(f'Прибыль по закрытой позиции {trade.getdataname()} Общая={trade.pnl:.2f}, Без комиссии={trade.pnlcomm:.2f}')

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(self.datas[0].datetime[0]) if not dt else dt  # Заданная дата или дата текущего бара
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def format_price(self, ticker, price):
        """
        Функция округления до шага цены step, сохраняя signs знаков после запятой
        print(round_custom_f(0.022636, 0.000005, 6)) --> 0.022635
        """
        step = self.p.info_tickers[ticker]['securities']['MINSTEP']  # сохраняем минимальный Шаг цены
        signs = self.p.info_tickers[ticker]['securities']['DECIMALS']  # сохраняем Кол-во десятичных знаков

        val = round(price / step) * step
        return float(("{0:." + str(signs) + "f}").format(val))


def get_some_info_for_tickers(tickers, live_prefix):
    """Функция для получения информации по тикерам"""
    info = {}
    for ticker in tickers:
        i = store.get_symbol_info(ticker)
        info[f"{live_prefix}{ticker}"] = i
    return info


if __name__ == '__main__':
    exchange = 'MOEX'  # Биржа
    live_prefix = 'MOEX.'  # префикс для выставления заявок в live

    symbols = ['SBER', 'POLY', 'GAZP', 'LKOH', 'ROSN', 'NVTK', 'GMKN', 'PLZL',]  # Тикеры в формате <Код тикера>

    store = MoexAlgoStore(login=ConfigMOEX.Login, password=ConfigMOEX.Password)  # Хранилище AlgoPack + авторизация на Московской Бирже

    cerebro = bt.Cerebro(quicknotify=True)  # Инициируем "движок" BackTrader

    # ----------------------------------------------------
    # Внимание! - Теперь это Live режим работы стратегии #
    # ----------------------------------------------------

    info_tickers = get_some_info_for_tickers(symbols, live_prefix)  # берем информацию о тикере (минимальный шаг цены, кол-во знаков после запятой)

    # live 1-минутные бары / таймфрейм M1
    timeframe = "M1"
    fromdate = dt.datetime.now() - dt.timedelta(days=30)
    for symbol in symbols:
        # data_loader = store.getdata(timeframe=bt.TimeFrame.Minutes,
        #                      compression=1,
        #                      dataname=symbol,
        #                      fromdate=fromdate,
        #                      live_bars=True)
        data = store.getdata(timeframe=bt.TimeFrame.Minutes, compression=1, dataname=symbol, fromdate=fromdate, live_bars=False)  # поставьте здесь True - если нужно получать live бары

        cerebro.adddata(data)  # Добавляем данные

    cerebro.addstrategy(NotifierStrategy, timeframe=timeframe, live_prefix=live_prefix, info_tickers=info_tickers)  # Добавляем торговую систему

    cerebro.run()  # Запуск торговой системы
    # cerebro.plot()  # Рисуем график - в live режиме не нужно
