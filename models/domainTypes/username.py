from models.domainTypes.domainType import DomainType
import re
class Username(DomainType):
    
    @staticmethod
    def validator(inputstr:str)->str:
        regexUsername=r"^[A-Za-z][A-Za-z0-9_'.-]{5,19}$"
        if re.match(regexUsername,inputstr):
            return None
        else:
            return "Username not valid\n must have a length of at least 5 characters\nmust be no longer than 20 characters\nmust be started with a letter\ncan contain letters (a-z), numbers (0-9), dashes (-), underscores (_), apostrophes ('), and periods (.)\nno distinguish between lowercase or uppercase letters"
        

    def __init__(self,value,superAdmin:bool=False):
        if not superAdmin and not self.validate(value):
            raise Exception("Username not valid\n must have a length of at least 5 characters\nmust be no longer than 20 characters\nmust be started with a letter\ncan contain letters (a-z), numbers (0-9), dashes (-), underscores (_), apostrophes ('), and periods (.)\nno distinguish between lowercase or uppercase letters")
        self.value=value
    pass
    def validate(self,value=None)->bool:
        val= self.value if value==None else value
        regexUsername=r"^[A-Za-z][A-Za-z0-9_'.-]{5,19}$"
        
        if re.match(regexUsername,val):
            
            return True
        return False