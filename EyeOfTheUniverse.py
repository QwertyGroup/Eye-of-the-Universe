import sys

from emoji import emojize

import telegram
from telegram.ext import *

from Core.Community import *
from Core.ExecCmds import *
from Core.Log import Log, IsLoggingEnabled

IsLoggingEnabled = True
community = Community()

def GO(bot, update):
    GUID = str(update.message.chat_id)
    if not community.Exist(GUID):
        community.New(GUID)
    indiv = community.Get(GUID)
    SendDimSelection(indiv, update)


def HandleQuery(bot, update):
    GUID = str(update.callback_query.from_user.id)
    Log(f'Handling: {GUID}')
    community.Get(GUID).Execute(update)


def HandleMessage(bot, update):
    GUID = str(update.message.chat_id)
    community.Get(GUID).ExecuteOnMessage(bot, update)


def main():
    BotToken = '390252714:AAE0YvbmlmPOkyPp-JbmW33ujEOuL8qOgAw'
    bot = telegram.Bot(token=BotToken)
    updater = Updater(token=BotToken)

    updater.dispatcher.add_handler(CommandHandler('start', GO))
    updater.dispatcher.add_handler(CommandHandler('go', GO))
    updater.dispatcher.add_handler(CallbackQueryHandler(HandleQuery))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, HandleMessage))

    updater.start_polling()
    print('Listening...')


if __name__ == "__main__":
    sys.exit(int(main() or 0))