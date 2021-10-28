from models.domainTypes.emailAddress import EmailAddress
from models.domainTypes.phoneNumber import PhoneNumber
from models.domainTypes.address import Address

class Client:
    id=0
    fullname=None
    emailAddress:EmailAddress=None
    mobilePhoneNumber:PhoneNumber=None
    address:Address=None
    created:str=None
    createdBy:int=0
    def __init__(self,_fullname,_emailaddress,_phonenumber,_address,id=0,_created:str=None,_createdBy:int=0):
        self.id=id
        self.fullname=_fullname
        self.emailAddress=_emailaddress
        self.mobilePhoneNumber=_phonenumber
        self.address=_address
        self.created=_created
        self.createdBy=_createdBy
        pass
