from re import U


class Log:
    id:int=0
    username:str
    userId:int
    date:str
    time:str
    description:str
    additionalInfo:str
    suspicious:int
    def __init__(self,id:int=0,username:str=None,userId:int=0,date:str=None, time:str=None,description:str=None,additionalInfo:str=None,suspicious:int=0):
        self.id=id
        self.username=username
        self.userId=userId
        self.date=date
        self.time=time
        self.description=description
        self.additionalInfo=additionalInfo
        self.suspicious=suspicious