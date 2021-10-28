from models.domainTypes.password import Password
from data.constants import Constants
from data.logger import Logger
from models.domainTypes.address import Address
from models.domainTypes.phoneNumber import PhoneNumber
from models.domainTypes.emailAddress import EmailAddress
from models.domainTypes.fullname import FullName
from data.encrypter import EncryptionProvider
from Console.consoleUtil import ConsoleUtility
from data.databaseWrapper import DatabaseWrapper, DatabaseWrapperProvider
from models.user import User 
from models.client import Client
from datetime import date, datetime
from models.advisor import Advisor

class AdviserConsole:
    def userPasswordReset(self):
        try:
            resList=DatabaseWrapperProvider.instance.select(User)
            found=False
            count=0
            for row in resList:
                if row[0]==self.user.id:
                    found=True
                    break
                count+=1

            if found:
                theUser=User(dictionary={
                    "id":resList[count][0],
                    "fullname":EncryptionProvider.instance.decrypt(resList[count][1]),
                    "username":EncryptionProvider.instance.decrypt(resList[count][2]),
                    "role":Constants.getRoleById(int(resList[count][3])),
                    "passwordHash":EncryptionProvider.instance.decrypt(resList[count][4])})
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
                Logger.log(self.user.username,
                        self.user.id,"A users password was reset",
                        f"User {username}'s password was reset ",0)
                if nonres:
                    print("User updated")
                else:
                    print("User not updated")
        except Exception as ex:
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
            Logger.log(self.user.username,
                self.user.id,"Created a client",
                f"Client {email} was created ",0)
        except Exception as ex:
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
            Logger.log(self.user.username,
                    self.user.id,"A client's identity was changed",
                    f"Client {fullname}'s password/fullname/username/role was changed ",0)
            if nonres:
                print("Client added")
            else:
                print("Client not added")
        except Exception as ex:
            print("❌ Something went wrong: ",ex)

    def searchForClient(self):
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
            print("❌ Something went wrong: ",ex)

    def exitConsole(self):
        exit()

    functionalitiesOfUser = {
    'A' : userPasswordReset,
    'B' : addClient,
    'C' : editClient,
    'D' : searchForClient,
    'E' : exitConsole
    }
    def __init__(self, user:Advisor) -> None:
        self.user=user
        print("Welcome Advisor {}.".format(self.user.username))
        while True:
            ConsoleUtility.showFuncDict(self.functionalitiesOfUser)
            self.contextSwitch(input("What task do you want to do {} ?".format(self.user.username)))

    def contextSwitch(self, userInput:str):
        if userInput.upper() in self.functionalitiesOfUser:
            self.functionalitiesOfUser.get(userInput.upper(), -1)(self)
        else:
            print("Choose an option from the list")

    