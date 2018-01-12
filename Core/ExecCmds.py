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
    indiv.Librarian.user = indiv
    #update.callback_query.edit_message_text(f'{indiv.Librarian.Name}')
    SendBoxChildrenView(indiv, update)


def SendView(indiv, update, items):
    markup = Gen.GenFileViewMkp(items)
    update.callback_query.edit_message_text("File Viewer", reply_markup=markup)
    indiv.NextExec = OnItemSelected 


def OnItemSelected(indiv, update):
    response = update.callback_query.data
    if response == 'New':
        SendBWDialog(indiv, update); return
    if response == 'Back':
        return
    if response == 'Edit':
        return

    indiv.WriteField('CurrentBox', response)
    SendBoxChildrenView(indiv, update)
           
    
def SendBWDialog(indiv,update):
    markup = Gen.GenBWDialogMkp()
    update.callback_query.edit_message_text('Create new:', reply_markup=markup)
    indiv.NextExec = OnBWSelected


def SendBoxChildrenView(indiv,update):
    items = indiv.Librarian.GetBoxChildren(indiv.ReadField('CurrentBox')) # GetBoxContents in Cloud Librarin <---
    SendView(indiv, update, items)


def OnBWSelected(indiv, update):
    response = update.callback_query.data
    if(response == 'Box'): 
        indiv.Librarian.CreateBox() 
        SendBoxChildrenView(indiv, update)
        return

    if(response == 'Wave'): print('Listening your message'); return # receive voice msg from user and save its id
       
    
    #update.callback_query.edit_message_text(f'{update.callback_query.data}')