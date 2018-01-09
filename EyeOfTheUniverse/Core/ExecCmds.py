from Core.Log import *
import Core.BtnGen as Gen
from Core.CloudLibrarian import *


def SendDimSelection(indiv, update):
    Log(f'Sending Dim selection: {indiv.GUID}')
    markup = Gen.GenDimSelMkp()
    update.message.reply_text("Place to warp:　　", reply_markup=markup)
    indiv.NextExec = OnDimSelected


def OnDimSelected(indiv, update):
    Librarians = {
        'Digital Expanse': DigitalExpanseL,
        'Steel Mountain': SteelMountainL
    }

    callbackData = update.callback_query.data
    indiv.Librarian = Librarians[callbackData]()
