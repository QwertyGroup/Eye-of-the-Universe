import sys
from datetime import datetime
from threading import Timer

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

def handle_sub(bot, update):
    community.subscribe(bot, update)


def enable_sub_service(bot):
    time_now = datetime.now()
    time_start_sending = datetime(time_now.year,time_now.month, time_now.day, time_now.hour, time_now.minute + 1)
    #time_start_sending = datetime(time_now.year,time_now.month, time_now.day, 13, 15, 10)
    time_delay = time_start_sending - time_now
    seconds = time_delay.total_seconds()
    if seconds < 0: seconds += 24 * 60 * 60
    print(seconds)
    
    Timer(seconds, community.time_to_notify_subs, [bot]).start()

def main():
    BotToken = '390252714:AAE0YvbmlmPOkyPp-JbmW33ujEOuL8qOgAw'
    bot = telegram.Bot(token=BotToken)
    updater = Updater(token=BotToken)

    updater.dispatcher.add_handler(CommandHandler('start', go))
    updater.dispatcher.add_handler(CommandHandler('go', go))
    updater.dispatcher.add_handler(CommandHandler('sub', handle_sub))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_query))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    enable_sub_service(bot)

    updater.start_polling()
    print('Listening...')


if __name__ == "__main__":
    sys.exit(int(main() or 0))