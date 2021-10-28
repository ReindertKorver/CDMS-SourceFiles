from data.backup import Backup
from models.domainTypes.fullname import FullName
from models.domainTypes.phoneNumber import PhoneNumber
from models.domainTypes.address import Address
from models.domainTypes.username import Username
from models.log import Log
from data.logger import Logger
from re import U
from data.constants import Constants
from models.domainTypes.password import Password
from models.domainTypes.emailAddress import EmailAddress
from data.encrypter import EncryptionProvider
from models.user import User
from data.databaseWrapper import DatabaseWrapper, DatabaseWrapperProvider
from datetime import datetime
from Console.consoleUtil import ConsoleUtility
from models.superadmin import SuperAdmin
from models.client import Client


class SuperAdminConsole:
    def checkUsersAndRoles(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(User)
            test=[EncryptionProvider.instance.decrypt(row[1])+" - "+EncryptionProvider.instance.decrypt(row[2])+" - "+Constants.getRoleById(int(row[3])) for row in resList]
            for i, option in enumerate(test) :
                print(f'  {str(i+1)}. {option}')
            ConsoleUtility.enter_to_continue()
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)
        
    def addUser(self):
        print("Form for adding a user provide the following details:")
        try:
            username=ConsoleUtility.validate_input(Username.validator,"Type a username: ")
            emailadress=ConsoleUtility.validate_input(EmailAddress.validator,"Type a emailaddress: ")
            fullname=ConsoleUtility.validate_input(FullName.validator,"Type a fullname (firstname lastname):")

            (i,option)=ConsoleUtility.select_option(Constants.getRoles(),"Select a role for the user: ")
            role=option
            password=ConsoleUtility.validate_input(Password.validator,"Type a password: ")

            createdBy=self.user.id
            created=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            newUser=User(EncryptionProvider.instance.encrypt(fullname),EncryptionProvider.instance.encrypt(username),EncryptionProvider.instance.encrypt(password),emailaddress=EncryptionProvider.instance.encrypt(emailadress))

            res=DatabaseWrapperProvider.instance.insertUserNew(newUser,role,createdBy,created)
            print("User created")
            Logger.log(self.user.username.value,
                self.user.id,"Created a user",
                f"User {username} was created ",0)
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong:",ex)

    def editUser(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(User)
            test=[EncryptionProvider.instance.decrypt(row[1])+" - "+EncryptionProvider.instance.decrypt(row[2])+" - "+Constants.getRoleById(int(row[3])) for row in resList]
            (i,option)=ConsoleUtility.select_option(test,"Select a user: ")
            print("Edit user: ",EncryptionProvider.instance.decrypt(resList[option][1]),"\n")
            (i,optionToChange)=ConsoleUtility.select_option(["username","fullname","password", "role","emailaddress"],"What information do you want to change?: ")
            theUser=User(dictionary={
                "id":resList[option][0],
                "fullname":EncryptionProvider.instance.decrypt(resList[option][1]),
                "username":EncryptionProvider.instance.decrypt(resList[option][2]),
                "role":Constants.getRoleById(int(resList[option][3])),
                "passwordHash":EncryptionProvider.instance.decrypt(resList[option][4]),
                "emailaddress":EncryptionProvider.instance.decrypt(resList[option][7])})
            username=theUser.username
            fullname=theUser.fullName
            password=theUser.passwordHash
            emailaddress=theUser.emailaddress
            role=Constants.getRoleIdByValue(theUser.role)
            if i=="username":
                username=ConsoleUtility.validate_input(Username.validator,"Type a username: ")
            elif i=="emailaddress":
                emailaddress=ConsoleUtility.validate_input(EmailAddress.validator,"Type a emailaddress: ")    
            elif i=="fullname":
                fullname=ConsoleUtility.validate_input(FullName.validator,"Type a fullname (firstname lastname):")
            elif i=="password":
                password=ConsoleUtility.validate_input(Password.validator,"Type a password: ")
            elif i=="role":
                (roleName,role)=ConsoleUtility.select_option(Constants.getRoles(),"Select a role for the user: ")
            else:
                pass
            theUser.username=EncryptionProvider.instance.encrypt(username)
            theUser.fullname=EncryptionProvider.instance.encrypt(fullname )
            theUser.emailaddress=EncryptionProvider.instance.encrypt(emailaddress)
            theUser.passwordHash=EncryptionProvider.instance.encrypt(password)
            theUser.role=role
            nonres=DatabaseWrapperProvider.instance.update(theUser)
            Logger.log(self.user.username.value,
                    self.user.id,"A users identity changed",
                    f"User {username}'s password/fullname/username/role was changed ",0)
            if nonres:
                print("User updated")
            else:
                print("User not updated")
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)

    def deleteUser(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(User)
            test=[EncryptionProvider.instance.decrypt(row[1])+" - "+EncryptionProvider.instance.decrypt(row[2]) for row in resList]
            (i,option)=ConsoleUtility.select_option(test,"Select a user: ")
            boolres=DatabaseWrapperProvider.instance.delete(User(id=resList[option][0]))
            Logger.log(self.user.username.value,
                    self.user.id,"A user was deleted",
                    f"User with id: {resList[option][0]} and username: {resList[option][2]} was deleted",0)
            if boolres:
                print("User deleted")
            else:
                print("User not deleted")
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)

    def userPasswordReset(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(User)
            test=[EncryptionProvider.instance.decrypt(row[1])+" - "+EncryptionProvider.instance.decrypt(row[2])+" - "+Constants.getRoleById(int(row[3])) for row in resList]
            (i,option)=ConsoleUtility.select_option(test,"Select a user: ")
            theUser=User(dictionary={
                "id":resList[option][0],
                "fullname":EncryptionProvider.instance.decrypt(resList[option][1]),
                "username":EncryptionProvider.instance.decrypt(resList[option][2]),
                "role":Constants.getRoleById(int(resList[option][3])),
                "passwordHash":EncryptionProvider.instance.decrypt(resList[option][4])})
            username=theUser.username
            fullname=theUser.fullName
            password=theUser.passwordHash
            role=Constants.getRoleIdByValue(theUser.role)
        
            password=ConsoleUtility.validate_input(Password.validator,"Type a password: ")
            
            theUser.username=EncryptionProvider.instance.encrypt(username)
            theUser.fullname=EncryptionProvider.instance.encrypt(fullname )
            theUser.passwordHash=EncryptionProvider.instance.encrypt(password)
            theUser.role=role
            nonres=DatabaseWrapperProvider.instance.update(theUser)
            Logger.log(self.user.username.value,
                    self.user.id,"A users password was reset",
                    f"User {username}'s password was reset ",0)
            if nonres:
                print("User updated")
            else:
                print("User not updated")
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)
    def createBackup(self):
        print("Creating backup")
        Backup.doBackup()
        
    def showLogs(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(Log,name="logging")
            print("Username:\tDate\t\tTime\t\tDescription\t\tAdditional Information\t\t\tSuspicious")
            test=[EncryptionProvider.instance.decrypt(row[1])+"\t"+row[3]+"\t"+row[4]+"\t"+EncryptionProvider.instance.decrypt(row[5])+"\t"+EncryptionProvider.instance.decrypt(row[6])+"\t"+("Yes" if row[7]==1 else "No") for row in resList]
            for i, option in enumerate(test) :
                print(f'  {str(i+1)}. {option}')
            ConsoleUtility.enter_to_continue()
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)
        
    def addClient(self):
        try:
            email=ConsoleUtility.validate_input(EmailAddress.validator,"Type a emailaddress: ")
            newClient = Client(
                EncryptionProvider.instance.encrypt(ConsoleUtility.validate_input(FullName.validator,"Type a fullname (firstname lastname): ")),
                EncryptionProvider.instance.encrypt(email),
                EncryptionProvider.instance.encrypt(ConsoleUtility.validate_input(PhoneNumber.validator,"Type a phonenumber +31-6-(DDDDDDDD): ")),
                EncryptionProvider.instance.encrypt(ConsoleUtility.validate_input(Address.validator,"Type a address (city street housenumber zipcode): ")),
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                self.user.id,
            )
        
            DatabaseWrapperProvider.instance.insert(newClient.__dict__, "client")
            Logger.log(self.user.username.value,
                self.user.id,"Created a client",
                f"Client {email} was created ",0)
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)
    
    def editClient(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(Client)
            test=[EncryptionProvider.instance.decrypt(row[1])+" - "+EncryptionProvider.instance.decrypt(row[2]) for row in resList]
            (i,option)=ConsoleUtility.select_option(test,"Select a client: ")
            print("Edit client: ",EncryptionProvider.instance.decrypt(resList[option][1]),"\n")
            (i,optionToChange)=ConsoleUtility.select_option(["fullname","emailaddress","address", "mobilephonenumber"],"What information do you want to change?: ")
            theClient=Client(_fullname=EncryptionProvider.instance.decrypt(resList[option][1]),
                            _emailaddress=EncryptionProvider.instance.decrypt(resList[option][2]),
                            _phonenumber= EncryptionProvider.instance.decrypt(resList[option][4]),
                            _address=EncryptionProvider.instance.decrypt(resList[option][3]),
                            id=resList[option][0],
                            _created=resList[option][6],
                            _createdBy=resList[option][5]
                            )
            fullname=theClient.fullname
            emailAddress=theClient.emailAddress
            address=theClient.address
            mobilePhoneNumber=theClient.mobilePhoneNumber
            if i=="fullname":
                fullname=ConsoleUtility.validate_input(FullName.validator,"Type a fullname (firstname lastname): ")
            elif i=="emailaddress":
                emailAddress=ConsoleUtility.validate_input(EmailAddress.validator,"Type a emailaddress: ")

            elif i=="address":
                address=ConsoleUtility.validate_input(Address.validator,"Type a address (city street housenumber zipcode): ")
            elif i=="mobilephonenumber":
                mobilePhoneNumber=ConsoleUtility.validate_input(PhoneNumber.validator,"Type a phonenumber +31-6-(DDDDDDDD):")
            else:
                pass
            theClient.fullname=EncryptionProvider.instance.encrypt(fullname)
            theClient.emailAddress=EncryptionProvider.instance.encrypt(emailAddress )
            theClient.address=EncryptionProvider.instance.encrypt(address)
            theClient.mobilePhoneNumber=EncryptionProvider.instance.encrypt(mobilePhoneNumber)
            nonres=DatabaseWrapperProvider.instance.update(theClient)
            Logger.log(self.user.username.value,
                    self.user.id,"A client's identity was changed",
                    f"Client {fullname}'s password/fullname/username/role was changed ",0)
            if nonres:
                print("Client updated")
            else:
                print("Client not updated")
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)
    

    def deleteClient(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(Client)
            test=[EncryptionProvider.instance.decrypt(row[1])+" - "+EncryptionProvider.instance.decrypt(row[2]) for row in resList]
            (i,option)=ConsoleUtility.select_option(test,"Select a client: ")
            boolres=DatabaseWrapperProvider.instance.delete(User(id=resList[option][0]))
            Logger.log(self.user.username.value,
                    self.user.id,"A client was deleted",
                    f"Client with id: {resList[option][0]} and emailaddress: {resList[option][2]} was deleted",0)
            if boolres:
                print("Client deleted")
            else:
                print("Client not deleted")
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)

    def searchClient(self):
        try:
            inp=ConsoleUtility.validate_input(FullName.validator,"Search for client emailaddress or fullname:")

            resList=DatabaseWrapperProvider.instance.select(Client)
            newList=[ row if inp in (EncryptionProvider.instance.decrypt(row[1])+" "+EncryptionProvider.instance.decrypt(row[2])) else None for row in resList ]
            
            for row1 in newList:
                if(row1!=None):
                    print(EncryptionProvider.instance.decrypt(row1[1]),
                    EncryptionProvider.instance.decrypt(row1[2]),
                    EncryptionProvider.instance.decrypt(row1[3]),
                    "+31-6-"+EncryptionProvider.instance.decrypt(row1[4]))
            ConsoleUtility.enter_to_continue()
        except Exception as ex:
            Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(ex),0)
            print("❌ Something went wrong: ",ex)

    def exitConsole(self):
        exit()

    functionalitiesOfUser = {
    'A' : checkUsersAndRoles,
    'B' : addUser,
    'C' : editUser,
    'D' : deleteUser,
    'E' : userPasswordReset,
    'F' : createBackup,
    'G' : showLogs,
    'H' : addClient,
    'I' : editClient,
    'J' : deleteClient,
    'K' : searchClient,
    'L' : exitConsole
    
    }
    def __init__(self, user:SuperAdmin) -> None:
        self.user=user
        print("Welcome SuperAdmin {}.".format(self.user.username))
        while True:
            try:
                ConsoleUtility.showFuncDict(self.functionalitiesOfUser)
                self.contextSwitch(input("What task do you want to do {} ?".format(self.user.username)))
            except KeyboardInterrupt:
                print("Canceled")
            except Exception as e:
                Logger.log(self.user.username.value,self.user.id,"Something went wrong",str(e),0)
                print("Something went wrong: " + str(e))
           


    def contextSwitch(self, userInput:str):
        if userInput.upper() in self.functionalitiesOfUser:
            self.functionalitiesOfUser.get(userInput.upper(), -1)(self)
        else:
            print("Choose an option from the list")
   
    
