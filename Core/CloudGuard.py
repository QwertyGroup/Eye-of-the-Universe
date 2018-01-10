import httplib2
import os

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage

SERVICE_SCOPE = ['https://www.googleapis.com/auth/drive']
PRIVATE_KEY_PATH = 'Storage/Goo/GooeySecret.json'
CREDENTIALS_STORAGE = os.path.join(os.path.dirname(PRIVATE_KEY_PATH), 'GooCred.json')


def GetGooCred():
    http = httplib2.Http()
    storage = Storage(CREDENTIALS_STORAGE)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(PRIVATE_KEY_PATH, SERVICE_SCOPE)
        storage.put(credentials)
    else:
        credentials.refresh(http)

    return credentials
