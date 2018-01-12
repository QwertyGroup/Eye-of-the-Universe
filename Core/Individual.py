from Core.Log import *
from Core.CloudLibrarian import Register

register = Register()

class Individual:
    def __init__(self, GUID):
        self.GUID = GUID
        self.NextExec = None
        self.Librarian = None
        self.regRow = None
        if register.Exist(self.GUID):  # Знает свое место
            self.regRow = register.ReadField(self, 'Row')
        else:
            self.regRow = register.Add(GUID)

    def Execute(self, update):
        if self.NextExec != None:
            Log(f"Executing delegate for: {self.GUID}")
            self.NextExec(self, update)
        else:
            Log(f"Delegate is empty. Can't exec. GUID: {self.GUID}")

    def Die(self):
        register.Remove(self.regRow)

    def ReadField(self, key):
        return register.ReadField(self, key)

    def WriteField(self, key, val):
        register.WriteField(self, key, val)
