import sys

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from core.community import Community

community = Community()

def go(bot, update):
    community.handle_login(bot, update)
    
def handle_query(bot, update):
    community.provide_query(bot, update)

def handle_message(bot, update):
    community.provide_message(bot, update)

def main():
    BotToken = '390252714:AAE0YvbmlmPOkyPp-JbmW33ujEOuL8qOgAw'
    bot = telegram.Bot(token=BotToken)
    updater = Updater(token=BotToken)

    updater.dispatcher.add_handler(CommandHandler('start', go))
    updater.dispatcher.add_handler(CommandHandler('go', go))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_query))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    print('Listening...')


if __name__ == "__main__":
    sys.exit(int(main() or 0))