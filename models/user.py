from models.domainTypes.domainType import DomainType
from models.domainTypes.emailAddress import EmailAddress
from models.domainTypes.phoneNumber import PhoneNumber
from models.domainTypes.password import Password
from models.domainTypes.address import Address
from models.domainTypes.username import Username


class User:
    id:int=0
    fullName=None
    username:Username=None
    emailaddress:EmailAddress=None
    passwordHash:Password=None
    userType="default"
    role="default"
    def __init__(self,fullname=None,username=None,password=None,id=0,dictionary:dict={},role="default",emailaddress=None):
        if dictionary!={}:
            self.id=dictionary["id"]if "id" in dictionary else None
            self.fullName=dictionary["fullname"]if "fullname" in dictionary else None
            self.username=dictionary["username"]if "username" in dictionary else None
            self.passwordHash=dictionary["passwordHash"]if "passwordHash" in dictionary else None
            self.role=dictionary["role"] if "role" in dictionary else None
            self.emailaddress=dictionary["emailaddress"] if "emailaddress" in dictionary else None
        else:
            self.id=id
            self.fullName=fullname
            self.username=username
            self.passwordHash=password
            self.role=role
            self.emailaddress=emailaddress
        pass
   