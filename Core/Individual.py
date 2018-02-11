import uuid

from core.pyre import ignite
from core.UI_generator import gen_branch_sel_mkp, gen_file_view_mkp, gen_bw_dialog_mkp

class Individual():
    pyre = ignite()

    def __init__(self, GUID):
        self.GUID = GUID
        self.nextExec = None
        self.msgHandler = None
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


    def send_markup(self, bot, update, markup, msg):
        if update.callback_query:
            update.callback_query.edit_message_text(msg, reply_markup=markup)
            
        if update.message:
            update.message.reply_text(msg, reply_markup=markup)

    def on_branch_selected(self, bot, update):
        callbackData = update.callback_query.data
        self.path = [self.GUID, callbackData]
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

            if self.GUID == self.path[-1]:
                self.on_login(bot, update)
                return

            self.open(bot, update, self.path[-1], self.current_path())
            return
        if callbackData == 'Edit':
            pass

        # else open box or maybe send wave
        self.path.append(callbackData)
        self.open(bot, update, callbackData, self.current_path())

    def on_bw_selected(self, bot, update):
        callbackData = update.callback_query.data

        itemGUID = None
        if callbackData == 'Box':
            itemGUID = self.create_new_box(bot, update)
        elif callbackData == 'Wave':
            pass

        self.nextExec = self.on_item_selected
        self.edgeItem = itemGUID
        self.msgHandler = self.on_rename

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
        #if 'exist' in items: items = None
        meta = self.load_meta(items)
        self.send_markup(bot, update, gen_file_view_mkp(items, meta), message)

    def path_to_string(self, path):
        return '/'.join(path) + '/'

    def current_path(self):
        return self.path_to_string(self.path)

    def update_path(self):
        self.pyre.child(self.GUID).update({'path': self.current_path()})

    def collect_items_from(self, directory):
        items = self.get_data_from(self.branch_path() + f'boxes/{directory}/')
        if 'exist' in items or not items: items = list()
        return items

    def load_meta(self, items):
        if not items: return {}
        meta = dict()
        for item in items:
            data = self.pyre.child(self.branch_path() + f'meta/{item}/').get()
            meta[item] = data.val()
        return meta
                
    def branch_path(self):
        return self.path_to_string(self.path[:2])