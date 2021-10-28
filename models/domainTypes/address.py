from models.domainTypes.domainType import DomainType
from data.constants import Constants


class Address(DomainType):
    @staticmethod
    def validator(inputstr:str)->str:
        arr=inputstr.split()
        if len(arr)==4:
            if str(arr[1])==None :
                return "Street is not valid"
            if not str(arr[1]).isalpha():
                return "Street is not valid"
            if str(arr[2])==None : 
                return "Housenumber is not valid"
            if not str(arr[2]).isdigit():
                return "Housenumber is not valid"
            if str(arr[3])==None :
                return "Zipcode is not valid should be DDDDXX"
            
            if len(str(arr[3]))!=6 :
                return "Zipcode is not valid should be DDDDXX"
            
            if not str(arr[3])[0:4].isdigit(): 
                return "Zipcode is not valid should be DDDDXX"

            if not str(arr[3])[4:6].isalpha():
                return "Zipcode is not valid should be DDDDXX"

            if str(arr[0])==None:
                return "City is not valid should be one of "+(", ".join(Constants.getCities()))

            if not Constants.validateCity(str(arr[0])):
                return "City is not valid should be one of "+(", ".join(Constants.getCities()))
            
            
            return None
        else:
            return "Type the address in four parts like (city street housenumber zipcode)"



    def __init__(self,street,houseNumber,zipCode,city):
        self.street=street
        self.houseNumber=houseNumber
        self.zipCode=zipCode
        self.city=city
        self.validate()
        self.value=str(street)+" "+str(houseNumber)+" "+str(city)+" "+str(zipCode)

    def validate(self)->bool:
        if str(self.street)==None and not str(self.street).isalpha():
            return False
        if str(self.houseNumber)==None and not str(self.street).isdigit():
            return False
        if str(self.zipCode)==None and len(str(self.zipCode))!=6 and not str(self.zipCode)[0:4].isalpha() and not str(self.zipCode)[4:6].isdigit():
            return False
        if str(self.city)==None and not Constants.validateCity(str(self.city)):
            return False
        if str(self.street)==None:
            return False