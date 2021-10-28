from models import user 
from Console.clientConsole import ClientConsole

class Console:
    def __init__(self):
        print("Good day to you, welcome to the Client Data Management System")

        username = input("What is your username?")
        password = input("what is your password?")

        self.signInUser = user("sdfsadf", "fsdfsdf", "fsdfsdf", "sdfsdfsdf", "fdsfsdf")

        if(signInUser.userType == "Client"):
            clientConsole(signInUser)

        if(signInUser.userType == "Advisors"):
            clientConsole(signInUser)

        if(signInUser.userType == "System Administrators"):
            clientConsole(signInUser)

        if(signInUser.userType == "Super Admin"):
            clientConsole(signInUser)





