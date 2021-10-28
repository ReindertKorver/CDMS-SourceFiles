from data.encrypter import EncryptionProvider
import datetime
from models.log import Log
from data.databaseWrapper import DatabaseWrapperProvider


class Logger:
    @staticmethod
    def log(username,userid,description, additonalinfo=None, suspicious=0):
        try:
            DatabaseWrapperProvider.instance.insert(Log(0,
                EncryptionProvider.instance.encrypt( username),
                userid,
                datetime.datetime.now().strftime("%d/%m/%Y"),
                datetime.datetime.now().strftime("%H:%M:%S"),
                EncryptionProvider.instance.encrypt(description),
                EncryptionProvider.instance.encrypt(additonalinfo),
                suspicious).__dict__,
                "logging")
        except:
                pass