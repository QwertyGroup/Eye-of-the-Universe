from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def GenDimSelMkp():  # Generate Dim Selection Markup
    kb = [[InlineKeyboardButton('🌌 DIGITAL  EXPANSE', callback_data='Digital Expanse')],
          [InlineKeyboardButton('🏔️ STEEL  MOUNTAIN', callback_data='Steel Mountain')]]
    dimSelMkp = InlineKeyboardMarkup(kb)
    return dimSelMkp
