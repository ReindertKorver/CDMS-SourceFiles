from models.domainTypes.domainType import DomainType


class PhoneNumber(DomainType):

    @staticmethod
    def validator(inputstr:str)->str:
        
        if len(str(inputstr))!=8 :
            return "Phonenumber should have a length of 8"
        elif not str(inputstr).isdigit():
             return "Phonenumber should only contain digits"
        else:
            return None
        
        
        return None
    def validate(self,value)->bool:
        val= self.value if value==None else value
        if len(str(val))!=8 and not str(val).isdigit():
            return False
        else:
            return True

    def __init__(self,value):
        
        if not self.validate(value):
            raise Exception('Value not valid phonenumber should be DDDDDDDD')
        self.value="+31-6-"+str(value)
    pass
    