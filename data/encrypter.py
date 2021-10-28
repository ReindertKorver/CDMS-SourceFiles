from os import stat

class Encrypter:
    
    def __init__(self, salt):
        self.salt=salt
    def encrypt(self, content):
        hashedContent=""
        for char in content:
            hashedContent+=chr(ord(char)-len(self.salt))
        return hashedContent
    def decrypt(self, hashedContent):
        content=""
        for char in hashedContent:
            content+=chr(ord(char)+len(self.salt))
        return content
class EncryptionProvider:
    @staticmethod
    def getGlobalEncriptifier()->Encrypter:
        return EncryptionProvider.instance
    @staticmethod
    def setGlobalEncriptifier(value):
        EncryptionProvider.instance:Encrypter=value