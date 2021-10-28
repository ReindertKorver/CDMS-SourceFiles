from models.domainTypes.domainType import DomainType


class FullName(DomainType):

    @staticmethod
    def validator(inputstr:str)->str:
        
        if len(str(inputstr))> 30:
            return "Fullname can not be longer then 30"
        elif not str(inputstr.replace(" ","")).isalpha():
             return "Fullname should only contain letters"
        else:
            return None
        