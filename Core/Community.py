from core.individual import Individual
from core.pyre import ignite
from core.currency_service import get_image, get_message

class Community:
    pyre = ignite()

    def __init__(self):
        self._localCommunity = dict()

    def new(self, GUID):
        self._localCommunity[GUID] = Individual(GUID)

    def delete(self, GUID):
        self._localCommunity[GUID].Die()
        del self._localCommunity[GUID]

    def exist(self, GUID):
        return GUID in self._localCommunity

    def get(self, GUID):
        if self.exist(GUID):
            return self._localCommunity[GUID]
        else:
            return None

    def send_notification(self, bot, update, message):
        if update.message: chat_id = message.chat_id
        if update.callback_query: chat_id = update.callback_query.message.chat_id
        bot.send_message(chat_id, message)

    def provide_query(self, bot, update):
        GUID = str(update.callback_query.from_user.id)
        if self.exist(GUID):
            self._localCommunity[GUID].on_query(bot, update)
        else:
            self.send_notification(bot, update, 'Starting new session:')
            self.handle_relogin(bot, update)

    def provide_message(self, bot, update):
        GUID = str(update.message.chat_id)
        self._localCommunity[GUID].on_message(bot, update)

    
    def handle_login(self, bot, update):
        GUID = str(update.message.chat_id)
        if not self.exist(GUID):
            self._localCommunity[GUID] = Individual(GUID)
        self._localCommunity[GUID].on_login(bot, update)

    def handle_relogin(self, bot, update):
        GUID = str(update.callback_query.message.chat_id)
        if not self.exist(GUID):
            self._localCommunity[GUID] = Individual(GUID)
        self._localCommunity[GUID].on_relogin(bot, update)

    def subscribe(self, bot, update):
        GUID = str(update.message.chat_id)
        self.add_sub(GUID)

    def add_sub(self, GUID):
        self.pyre.child(f'subscribers/{GUID}').update({'exist':True})

    def get_subs(self):
        response = self.pyre.child('subscribers').get().val().items()
        subs = [sub[0] for sub in response]
        return subs

    def time_to_notify_subs(self, bot):
        message = get_message()
        image = get_image()
        subs = self.get_subs()
        for sub in subs:
            for msg in message.split('*message_separator*'):
                if msg and msg != '' and msg != '\n':
                    bot.send_message(sub, msg)
            #bot.send_photo(sub, image)
        print('just in time.')
