from emoji import emojize

import telegram
from telegram.ext import *

from Core.Community import *
from Core.ExecCmds import *


# Init Bot
BotToken = '390252714:AAE0YvbmlmPOkyPp-JbmW33ujEOuL8qOgAw'
bot = telegram.Bot(token=BotToken)
updater = Updater(token=BotToken)

print('In')
# Init DataBase
community = Community()


def GO(bot, update):
    GUID = str(update.message.chat_id)
    if not community.Exist(GUID):
        community.New(GUID)
    indiv = community.Get(GUID)
    SendDimSelection(indiv, update)


def HandleQuery(bot, update):
    print('here -1')
    GUID = str(update.callback_query.from_user.id)
    Log(f'Handling: {GUID}')
    community.Get(GUID).Execute(update)

    print('here0')
    me = commutiny.Get(GUID)
    print('here1')
    me.Die()  # rofl )0)) hmm didnt work(
    print('here2')


updater.dispatcher.add_handler(CommandHandler('start', GO))
updater.dispatcher.add_handler(CommandHandler('go', GO))
updater.dispatcher.add_handler(CallbackQueryHandler(HandleQuery))


updater.start_polling()
