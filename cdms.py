from Console.systemAdminConsole import SystemAdminConsole
from Console.adviserConsole import AdviserConsole
from data.logger import Logger
from models.log import Log
from Console.superAdminConsole import SuperAdminConsole
from models.user import User
from models.domainTypes.emailAddress import EmailAddress
from data.constants import Constants
import re
import datetime
from models.domainTypes.password import Password
from data.databaseWrapper import DatabaseWrapper, DatabaseWrapperProvider
from data.encrypter import Encrypter, EncryptionProvider
from Console.console import Console

dbWrapper= DatabaseWrapper("appDB.db")
dbWrapper.initializeDatabase()
sprAdmin=Constants.getSuperAdmin()
encryptifier= Encrypter(str(sprAdmin.username)+str(sprAdmin.passwordHash))
DatabaseWrapperProvider.setGlobalDbWrapper(dbWrapper)
EncryptionProvider.setGlobalEncriptifier(encryptifier)
print("If the message below equals hello world then the encryption is working properly:")
res= encryptifier.decrypt(encryptifier.encrypt("hello world"))
print(res)

res1= encryptifier.decrypt(res)
programMode="UnAuthenticated"
user:User=None
while True:
    username = input("Username:")
    passwd = input("Password:")
    
    if username==str(sprAdmin.username) and passwd==str(sprAdmin.passwordHash):
        programMode=sprAdmin.userType
        user=sprAdmin
        Logger.log(user.username, user.id,"Logged in","",0)
        break
    else:
        otherUser = dbWrapper.checkUser(username,passwd)

        if(otherUser != None):
            user=otherUser
            programMode = otherUser.userType
            Logger.log(user.username, user.id,"Logged in","",0)
            break
        else:
            Logger.log(username,
                0,"Unsuccesful login",
                f"User {username} tried to login with {passwd}",1)
            print("Wrong username or password")

if programMode=="superadmin":
    SuperAdminConsole(user)
elif programMode=="systemadmin":
    SystemAdminConsole(user)
elif programMode=="advisor":
    AdviserConsole(user)
   
    
