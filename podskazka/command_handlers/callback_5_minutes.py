from telegram.ext import ContextTypes
from datetime import datetime


def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    tools = context.job.data['tools']
    for tool in tools:
        messages = tool.update()

        print('^^^', datetime.now().isoformat(), tool.name, 'updated!')

        for message in messages:
            context.bot.send_message(chat_id='403165653', text=message if message else f'{tool.name} updated!')
