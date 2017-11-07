import telegram
import time
from telegram.ext import *

TACCKEN = '390252714:AAE0YvbmlmPOkyPp-JbmW33ujEOuL8qOgAw'

bot = telegram.Bot(token=TACCKEN)
print(f'{bot.get_me().first_name} was inited!')
updater = Updater(token=TACCKEN)
dispatcher = updater.dispatcher


def OnStart(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def Echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


dispatcher.add_handler(CommandHandler('start', OnStart))
dispatcher.add_handler(MessageHandler(Filters.text, Echo))

updater.start_polling()
