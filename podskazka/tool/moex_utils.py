import requests
from datetime import datetime, timedelta
import pandas as pd
from moexalgo import session


def fetch_trade_data(ticker:str=None, tradeno=None, date=datetime.now().date().strftime('%Y-%m-%d')):
    if not ticker:
        raise Exception('Не возможно получить данные торговым сделкам. Тикер не задан')

    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}/trades.json"

    if tradeno:
        url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}/trades.json?tradeno={tradeno}&date={date}"

    # Define the cookies for authorization
    cookies = {
        'MicexPassportCert': session.AUTH_CERT
    }

    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()  # Raise an error for bad status codes
        # Print the JSON data_loader
        data = response.json()

        columns = data['trades']['columns']
        trades_data = data['trades']['data']

        return pd.DataFrame(data=trades_data, columns=columns)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def get_all_trades(ticker:str, start_tradeno:int):
    trades_data = fetch_trade_data(ticker=ticker, tradeno=start_tradeno)

    if len(trades_data) == 0:
        raise Exception('get_all_trades: Trades data not loaded!')

    if len(trades_data) < 5000:
        return trades_data

    while True:
        new_trades_data = fetch_trade_data(ticker=ticker, tradeno=start_tradeno)
        trades_data = pd.concat([trades_data, new_trades_data])
        start_tradeno = trades_data.iloc[-1]['TRADENO']

        if len(new_trades_data) < 5000:
            break

    return trades_data


def get_tick_trade_data(ticker=None,  # название тикера
                         start_tradeno=None,  # Начальный номер торговой сделки с которого получать данные о сделках
                         start_datetime=None,  # время с которого получать данные (пока не работает)
                         date=None  # дата на которую получать данные, если не указать, будет текущая дата
                         ):
    if not start_datetime and not start_tradeno:
        get_all_trades(ticker=ticker, start_tradeno=start_tradeno)

    if not start_tradeno and start_datetime:
        start_tradeno = get_tradeno_by_datetime(start_datetime)

    trade_data = fetch_trade_data(tradeno=start_tradeno, date=date)

    return trade_data


def get_tradeno_by_datetime(daytime):
    # TODO это нужно переделать когда понадобится функуионал
    return 10536621001


def price_shift(df):
    return (df['PRICE'][0] - df['PRICE'].iloc[-1]) / df['PRICE'].iloc[-1] * 100


def buy_sell(df):
    sums = df.groupby('BUYSELL')['QUANTITY'].sum()

    # Get the sum for 'B' and 'S', defaulting to 0 if they don't exist
    buy_sum = sums.get('B', 0)
    sell_sum = sums.get('S', 0)

    return buy_sum, sell_sum
