from os import stat
from models.domainTypes.password import Password
from models.domainTypes.emailAddress import EmailAddress

class Constants:
    @staticmethod
    def getRoleById(id:int):
        if id<2:
            return ["systemadmin","advisor"][id]
        else:
            return None
    @staticmethod
    def getRoleIdByValue(value:str):
        return ["systemadmin","advisor"].index(value)
    @staticmethod
    def getRoles():
        return ["systemadmin","advisor"]
    @staticmethod
    def getSuperAdmin():
        from models.superadmin import SuperAdmin
        return SuperAdmin(None,"superadmin","Admin!23",id=-9999)
    @staticmethod
    def getCities():
        return ["Amsterdam","Rotterdam","Utrecht","Maastricht","Delft","Den Haag","Haarlem","Arnhem","Breda","Eindhoven"]
    @staticmethod
    def validateCity(itemToCheck:str)->bool:
        return itemToCheck.lower() in [a.lower() for a in Constants.getCities()]
    

    