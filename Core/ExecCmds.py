from Core.Log import *
import Core.BtnGen as Gen
from Core.CloudLibrarian import *


def SendDimSelection(indiv, update):
    Log(f'Sending Dim selection: {indiv.GUID}')
    markup = Gen.GenDimSelMkp()
    if update.message != None: update.message.reply_text("Place to warp:　　", reply_markup=markup)
    if update.callback_query != None: update.callback_query.edit_message_text("Place to warp:　　", reply_markup=markup)
    indiv.NextExec = OnDimSelected


def OnDimSelected(indiv, update):
    Librarians = {
        'Digital Expanse': DigitalExpanseL,
        'Steel Mountain': SteelMountainL
    }

    callbackData = update.callback_query.data
    indiv.Librarian = Librarians[callbackData]()
    indiv.Librarian.user = indiv
    BootUp(indiv, update)


def SendView(indiv, update, items, msg="File Viewer"):
    markup = Gen.GenFileViewMkp(items)
    if update.callback_query != None:
        update.callback_query.edit_message_text(msg, reply_markup=markup)
    if update.message != None:
        update.message.reply_text(msg, reply_markup=markup)
    indiv.NextExec = OnItemSelected 


def OnItemSelected(indiv, update):
    response = update.callback_query.data
    if response == 'New':
        SendBWDialog(indiv, update); return
    
    if response == 'Back':
        Back(indiv, update); return
    
    if response == 'Edit': return

    OpenBox(indiv, update, response)

      
def OpenBox(indiv, update, boxGUID):
    indiv.WriteField('Path', indiv.ReadField('Path') + ':' + str(boxGUID))
    indiv.WriteField('CurrentBox', boxGUID)
    SendBoxChildrenView(indiv, update)
    

def BootUp(indiv, update):
    current = indiv.ReadField('CurrentBox')
    
    if current == '': boxGUID = indiv.GUID
    else: boxGUID = current
    
    if indiv.ReadField('Path') == '': indiv.WriteField('Path', indiv.ReadField('Path') + ':' + str(boxGUID))
    indiv.WriteField('CurrentBox', boxGUID)
    SendBoxChildrenView(indiv, update)


def Back(indiv,update):
    path = [str(i) for i in indiv.ReadField('Path').split(':')]
    parentBox = path[-2]
    path.pop()
    path = ':'.join(path)
    indiv.WriteField('CurrentBox', parentBox)
    indiv.WriteField('Path', path)
    if parentBox == '': SendDimSelection(indiv, update); return
    SendBoxChildrenView(indiv, update)


def SendBWDialog(indiv,update):
    markup = Gen.GenBWDialogMkp()
    update.callback_query.edit_message_text('Create new:', reply_markup=markup)
    indiv.NextExec = OnBWSelected


def SendBoxChildrenView(indiv,update, msg=None):
    items = indiv.Librarian.GetBoxChildren(indiv.ReadField('CurrentBox')) # GetBoxContents in Cloud Librarin <---
    if msg != None: SendView(indiv, update, items, msg)
    else: SendView(indiv, update, items)

def OnBWSelected(indiv, update):
    response = update.callback_query.data
    if(response == 'Box'): 
        indiv.Librarian.CreateBox() 
        SendBoxChildrenView(indiv, update, 'Enter box name:')
        return

    if(response == 'Wave'): print('Listening your message'); return # receive voice msg from user and save its id