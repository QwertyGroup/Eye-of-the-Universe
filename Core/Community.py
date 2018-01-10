from Core.Individual import *
from Core.Log import *
from Core.CloudLibrarian import Register

register = Register()


class Community:
    def __init__(self):
        self._localCommunity = dict()
        for GUID in register.Community():
            self._localCommunity[GUID] = Individual(GUID)

    def New(self, GUID):
        self._localCommunity[GUID] = Individual(GUID)

    def Del(self, GUID):
        self._localCommunity[GUID].Die()
        del self._localCommunity[GUID]

    def Exist(self, GUID):
        return GUID in self._localCommunity

    def Get(self, GUID):
        if self.Exist(GUID):
            return self._localCommunity[GUID]
        else:
            return None
