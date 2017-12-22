import telegram
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize

import time
import os


TACCKEN = '390252714:AAE0YvbmlmPOkyPp-JbmW33ujEOuL8qOgAw'

bot = telegram.Bot(token=TACCKEN)
print(f'{bot.get_me().first_name} was inited!')
updater = Updater(token=TACCKEN)
dispatcher = updater.dispatcher


def OnStartCmd(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


dispatcher.add_handler(CommandHandler('start', OnStartCmd))

updater.start_polling()
