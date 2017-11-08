import telegram
import time
import os
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
    bot.send_message(chat_id=update.message.chat_id, text=update.message.audio)
    print(update.message.text)
    print(update.message)


def AudioRepl(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Music")
    print('Auido file received')


def VoiceRepl(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="VoiceRepl")
    print('VoiceRepl file received')
    ans = f'{update.message.voice.duration}, {update.message.voice.mime_type}'
    print(ans)
    bot.send_message(chat_id=update.message.chat_id, text=ans)


def OnTestMessage(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="OnTestMessageStart")
    directory = os.path.dirname('tmp/')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('tmp/file.txt', 'w') as fi:
        fi.write('which is always equal to the length of the string')

    with open('tmp/file.txt') as fi:
        lines = fi.readlines()
        print(lines)
        bot.send_message(chat_id=update.message.chat_id, text=lines)

    time.sleep(5)
    os.remove('tmp/file.txt')
    os.rmdir('tmp/')
    print('deleted.')


dispatcher.add_handler(CommandHandler('start', OnStart))
dispatcher.add_handler(CommandHandler('test!', OnTestMessage))

dispatcher.add_handler(MessageHandler(Filters.text, Echo))
dispatcher.add_handler(MessageHandler(Filters.audio, AudioRepl))
dispatcher.add_handler(MessageHandler(Filters.voice, VoiceRepl))

updater.start_polling()
