from models.domainTypes.domainType import DomainType
import re
class Password(DomainType):
    @staticmethod
    def validator(inputSTR:str)->str:
        regexPassword=r"^(?=(?:.*[A-Z]){1,})(?=(?:.*[a-z]){1,})(?=(?:.*\d){1,})(?=(?:.*[~!@#$%^&*_\-+=`|\(){}\[\]:;'<>,.?/]){1,})([A-Za-z0-9~!@#$%^&*_\-+=`|\(){}\[\]:;'<>,.?/]{8,30})$"
        
        if re.match(regexPassword,inputSTR):
            return None
        
        return "Value not valid password should: \n have a length of at least 8 characters\nbe no longer than 30 characters\ncan contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%^&*_-+=`|\(){}[]:;\'<>,.?/\nmust have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character"

    def __init__(self,value,superAdmin:bool=False):
        if not superAdmin and not self.validate(value):
            raise Exception('Value not valid password should: \n have a length of at least 8 characters\nbe no longer than 30 characters\ncan contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%^&*_-+=`|\(){}[]:;\'<>,.?/\nmust have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character')
       
        self.value=value
        pass
    def validate(self,value):
        val= self.value if value==None else value
        if val==None:
            print("Silly is none")
            return False
        # if len(self.value)<8:
        #     return False
        # if len(self.value)>30:
        #     return False

        regexPassword=r"^(?=(?:.*[A-Z]){1,})(?=(?:.*[a-z]){1,})(?=(?:.*\d){1,})(?=(?:.*[~!@#$%^&*_\-+=`|\(){}\[\]:;'<>,.?/]){1,})([A-Za-z0-9~!@#$%^&*_\-+=`|\(){}\[\]:;'<>,.?/]{8,30})$"
        
        if re.match(regexPassword,val):
            print("Silly ")
            return True
        
        return False
    pass