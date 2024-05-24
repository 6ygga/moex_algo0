import os, json
from dotenv import load_dotenv
from moexalgo import session
from telegram.ext import ApplicationBuilder, CommandHandler, _jobqueue
from command_handlers.hello import hello
from command_handlers.start import start
from command_handlers.callback_5_minutes import callback_minute
from Psymbol import Psymbol


load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN', '')

if __name__ == '__main__':
    session.authorize(os.getenv('LOGIN'), os.getenv('PASSWORD'))

    f = open('./data.json', 'r')
    data = json.load(f)
    # symbols = ['SBER', 'POLY', 'GAZP', 'LKOH', 'ROSN', 'NVTK', 'GMKN', 'PLZL',]  # Тикеры в формате <Код тикера>
    tools = []
    for symbol in data['symbols']:
        tools.append(Psymbol(symbol))

    telegram_app = ApplicationBuilder().token(telegram_token).read_timeout(60).write_timeout(60).build()

    job_queue = telegram_app.job_queue
    job_minute = job_queue.run_repeating(callback_minute, interval=300, first=5, data={'tools': tools})

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("hello", hello))

    print('Bot started')
    telegram_app.run_polling()
