from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def gen_branch_sel_mkp():  # Generate Dim Selection Markup
    kb = [[InlineKeyboardButton('🌌 DIGITAL  EXPANSE', callback_data='Digital Expanse')],
          [InlineKeyboardButton('🏔️ STEEL  MOUNTAIN', callback_data='Steel Mountain')]]
    dimSelMkp = InlineKeyboardMarkup(kb)
    return dimSelMkp

def gen_file_view_mkp(items, meta):
    cmdline = [InlineKeyboardButton('Back', callback_data='Back'),
               InlineKeyboardButton('New', callback_data='New'),
               InlineKeyboardButton('Edit', callback_data='Edit')]

    kb = list()
    pairline = list()
    if items and meta:
        for item in items:
            if meta[item]['type'] == 'box':
                pairline.append(InlineKeyboardButton(f'🕋 {meta[item]["name"]}', callback_data=item))
            if meta[item]['type'] == 'wave':
                pairline.append(InlineKeyboardButton(f'💨 {meta[item]["name"]}', callback_data=item))                
            if len(pairline) == 2:
                kb.append(pairline)
                pairline = list()

    kb.append(cmdline)
    fileViewMkp = InlineKeyboardMarkup(kb)
    return fileViewMkp

#def gen_file_view_mkp(items, meta): # make this pretty
#    kb = [InlineKeyboardButton('Back', callback_data='Back'),
#          InlineKeyboardButton('New', callback_data='New'),
#          InlineKeyboardButton('Edit', callback_data='Edit')]

#    if items and meta:
#        waves = [InlineKeyboardButton(f'💨 {meta[item]["name"]}', callback_data=item)
#                      for item in items if meta[item]['type'] == 'wave']
#        if waves:
#            waves.reverse()
#            for wave in waves:
#                kb.insert(0, wave)

#        boxes = [InlineKeyboardButton(f'🕋 {meta[item]["name"]}', callback_data=item)
#                      for item in items if meta[item]['type'] == 'box']
#        if boxes:
#            boxes.reverse()
#            for box in boxes:
#                kb.insert(0, box)
      
#    fileViewMkp = InlineKeyboardMarkup([[item] for item in kb])
#    return fileViewMkp
def gen_bw_dialog_mkp():
    kb = [[InlineKeyboardButton('Box 🕋', callback_data='Box'),
           InlineKeyboardButton('Wave 💨', callback_data='Wave')]]
    dialogMkp = InlineKeyboardMarkup(kb)
    return dialogMkp