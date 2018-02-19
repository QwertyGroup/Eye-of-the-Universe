import uuid

from core.pyre import ignite
from core.UI_generator import gen_branch_sel_mkp, gen_file_view_mkp, gen_bw_dialog_mkp, gen_cancel_mkp, gen_del_rename_mkp, gen_rename_mkp, gen_delete_mkp

class Individual():
    pyre = ignite()

    def __init__(self, GUID):
        self.GUID = GUID
        self.nextExec = None
        self.msgHandler = None
        self.vceHandler = None
        self.path = [GUID] # [0] - id, [1] - branch, [-1] - last folder
        self.update_path()

    def die(self):
        self.pyre.child(self.GUID).remove()
        
    def on_login(self, bot, update):
        self.send_markup(bot, update, gen_branch_sel_mkp(), 'Place to warp:　　')
        self.nextExec = self.on_branch_selected

    def on_relogin(self, bot, update):
         if update.callback_query:
            update.callback_query.message.reply_text('Place to warp:　　', 
                                                     reply_markup=gen_branch_sel_mkp())
         self.nextExec = self.on_branch_selected

    def on_query(self, bot, update):
        self.nextExec(bot, update)

    def on_message(self, bot, update):
        message = update.message.text
        self.msgHandler(bot, update, message)
        self.msgHandler = None

    def on_voice(self, bot, update):
        self.vceHandler(bot, update)


    def send_markup(self, bot, update, markup, msg):
        if update.callback_query:
            update.callback_query.edit_message_text(msg, reply_markup=markup)
            
        if update.message:
            update.message.reply_text(msg, reply_markup=markup)

    def on_branch_selected(self, bot, update):
        callbackData = update.callback_query.data
        if callbackData == 'Steel Mountain':
            self.path = [self.GUID, callbackData]
        if callbackData == 'Digital Expanse':
            self.path = [callbackData]
        self.update_path()
        self.open(bot, update, callbackData, self.current_path())
        self.nextExec = self.on_item_selected

    def on_item_selected(self, bot, update):
        callbackData = update.callback_query.data

        if callbackData == 'New':
            self.send_markup(bot, update, gen_bw_dialog_mkp(), 'Select & enter item name')
            self.nextExec = self.on_bw_selected
            return
        if callbackData == 'Back':
            self.path.pop()
            if not self.path or self.GUID == self.path[-1]:
                self.on_login(bot, update)
                return
            self.open(bot, update, self.path[-1], self.current_path())
            return
        if callbackData == 'Edit':
            self.send_markup(bot, update, gen_del_rename_mkp(), 'Select an action:    ')
            self.nextExec = self.on_edit

        # else open box or maybe send wave
        meta = self.load_meta([callbackData])[callbackData]
        if meta['type'] == 'box':
            self.path.append(callbackData)
            self.open(bot, update, callbackData, self.current_path())
        if meta['type'] == 'wave':
            bot.forwardMessage(chat_id=update.callback_query.message.chat_id,
                               from_chat_id=meta['chatId'],
                               message_id=meta['msgId'])

    def on_edit(self, bot, update):
        callbackData = update.callback_query.data
        if callbackData == 'Rename' or callbackData == 'Del':
            items = self.latest_items
            meta = self.latest_meta
            if callbackData == 'Rename':
                self.send_markup(bot, update, gen_rename_mkp(items, meta), 'Rename')
                self.nextExec = self.on_rename_selected
            elif callbackData == 'Del': 
                self.send_markup(bot, update, gen_delete_mkp(items, meta), 'Delete')
                self.nextExec = self.on_del_selected
        elif callbackData == 'Cancel':
            self.on_voice_canceled(bot, update) # will work just as is

    def on_canceled(self, bot, update):
        self.send_markup(bot, update, gen_file_view_mkp(items, meta), message)
        self.open(bot, update, self.path[-1], self.current_path())
        self.nextExec = self.on_item_selected
        self.msgHandler = None
        self.vceHandler = None


    def on_rename_selected(self, bot, update):
         callbackData = update.callback_query.data
         if callbackData == 'Cancel':
            self.on_voice_canceled(bot, update)
         else:
            print(callbackData)

    def on_del_selected(self, bot, update):
        callbackData = update.callback_query.data
        if callbackData == 'Cancel':
            self.on_voice_canceled(bot, update)
        else:
            print(callbackData)

    def on_bw_selected(self, bot, update):
        callbackData = update.callback_query.data

        itemGUID = None
        if callbackData == 'Box':
            itemGUID = self.create_new_box(bot, update)
            self.edgeItem = itemGUID
            self.nextExec = self.on_item_selected
            self.msgHandler = self.on_rename
        elif callbackData == 'Wave':
            self.listen_new_wave(bot, update)
        elif callbackData == 'Cancel':
            self.open(bot, update, self.path[-1], self.current_path())
            self.nextExec = self.on_item_selected
            return


    def listen_new_wave(self, bot, update):
        self.send_markup(bot, update, gen_cancel_mkp(), "Ready. Please send us a voice message.")
        self.vceHandler = self.on_wave_received
        self.msgHandler = self.on_rename
        self.nextExec = self.on_voice_canceled 

    def on_voice_canceled(self, bot, update):
        callbackData = update.callback_query.data
        if callbackData == 'Cancel':
            self.open(bot, update, self.path[-1], self.current_path())
            self.nextExec = self.on_item_selected
            self.vceHandler = None
            self.msgHandler = None


    def on_wave_received(self, bot, update):
        wave_uuid = str(uuid.uuid4())
        msgId = update.message.message_id
        chatId = update.message.chat_id
        self.pyre.update({self.branch_path() + f'boxes/{self.path[-1]}/': self.collect_items_from(self.path[-1]) + [wave_uuid]})
        self.pyre.child(self.branch_path() + f'meta/{wave_uuid}').update({'name':'new wave', 'type':'wave', 'chatId':chatId, 'msgId':msgId})
        self.edgeItem = wave_uuid
        self.msgHandler = self.on_rename
        self.open(bot, update, self.path[-1], self.current_path())
        self.nextExec = self.on_item_selected
        self.vceHandler = None

    def on_rename(self, bot, update, newName):
        self.rename_item(self.edgeItem, newName)
        self.msgHandler = None
        self.open(bot, update, self.path[-1], self.current_path())

    def rename_item(self, itemGUID, newName):
        path = self.branch_path() + f'meta/{itemGUID}/'
        data = self.get_data_from(path)
        data['name'] = newName
        self.pyre.child(path).update(data)

    def get_data_from(self, path):
        return self.pyre.child(path).get().val()

    def create_new_box(self, bot, update):
        box_uuid = str(uuid.uuid4())
        self.pyre.child(self.branch_path() + f'boxes/{box_uuid}').update({'exist':True})
        self.pyre.update({self.branch_path() + f'meta/{box_uuid}/': {'name':'new box', 'type':'box'},
                          self.branch_path() + f'boxes/{self.path[-1]}/':
                          self.collect_items_from(self.path[-1]) + [box_uuid]})
        self.open(bot, update, self.path[-1], self.current_path())
        return box_uuid

    def open(self, bot, update, directory, message):
        items = self.collect_items_from(directory)
        meta = self.load_meta(items)
        self.latest_items = items
        self.latest_meta = meta
        self.send_markup(bot, update, gen_file_view_mkp(items, meta), message)

    def path_to_string(self, path):
        return '/'.join(path) + '/'

    def current_path(self):
        return self.path_to_string(self.path)

    def update_path(self):
        self.pyre.child(self.GUID).update({'path': self.current_path()})

    def collect_items_from(self, directory): 
        items = self.get_data_from(self.branch_path() + f'boxes/{directory}/')
        if  not items or 'exist' in items: items = list()
        return items

    def load_meta(self, items):
        if not items: return {}
        meta = dict()
        for item in items:
            data = self.pyre.child(self.branch_path() + f'meta/{item}/').get()
            meta[item] = data.val()
        return meta
                
    def branch_path(self):
        if self.path[0] == 'Digital Expanse':
            return self.path_to_string(self.path[:1])
        else:
            return self.path_to_string(self.path[:2])