from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def GenDimSelMkp():  # Generate Dim Selection Markup
    kb = [[InlineKeyboardButton('🌌 DIGITAL  EXPANSE', callback_data='Digital Expanse')],
          [InlineKeyboardButton('🏔️ STEEL  MOUNTAIN', callback_data='Steel Mountain')]]
    dimSelMkp = InlineKeyboardMarkup(kb)
    return dimSelMkp

def GenFileViewMkp(items): # make this pretty
    kb = [InlineKeyboardButton(f'🕋 {item.name}',callback_data=item.GUID) 
          for item in items if item.type == 'box']
    kb += [InlineKeyboardButton(f'💨 {item.name}',callback_data=item.GUID) 
          for item in items if item.type == 'wave']
    kb += [InlineKeyboardButton('Back',callback_data='Back'),
           InlineKeyboardButton('New',callback_data='New'),
           InlineKeyboardButton('Edit',callback_data='Edit')]
          
    fileViewMkp = InlineKeyboardMarkup([[item] for item in kb])
    return fileViewMkp

def GenBWDialogMkp():
    kb = [[InlineKeyboardButton('Box 🕋',callback_data='Box'),
           InlineKeyboardButton('Wave 💨',callback_data='Wave')]]
    dialogMkp = InlineKeyboardMarkup(kb)
    return dialogMkp