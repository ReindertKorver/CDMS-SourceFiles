from data.constants import Constants
from typing import Any
from models.client import Client
from models.advisor import Advisor
from models.domainTypes.password import Password
from models.domainTypes.emailAddress import EmailAddress
from models.domainTypes.username import Username
from models.systemadmin import SystemAdmin
from data.encrypter import Encrypter, EncryptionProvider
from models.user import User
import os

from Console.consoleUtil import ConsoleUtility
from data.database import Database



class DatabaseWrapper:

    def __init__(self, connectionString):
        self.connectionString=connectionString
        self.db= Database(connectionString)

    def initializeDatabase(self):
        print("Checking for legitimate database...")
        try:
            testRes = self.db.executeResultingQuery("SELECT name FROM sqlite_master WHERE type='table';")
            counter=0
            
            for row in testRes:
                if row[0] in ["client","user","logging"]:
                    counter+=1
        except:
            counter=0

        continueSetup=False
        compatibleDb=False
        if counter==3:
            ConsoleUtility.rewriteLastLine("✔️ Checking for legitimate database... COMPLETED succesfully ")
            compatibleDb=True
        elif counter==0:
            ConsoleUtility.rewriteLastLine("✔️ Checking for legitimate database... COMPLETED succesfully ")
            compatibleDb=True
        else:
            ConsoleUtility.rewriteLastLine("❌ Checking for legitimate database... COMPLETED unsuccesfully ")
            compatibleDb=False
            
        if not compatibleDb:
            choice =input("\nThe database is not compatible do you want to overwrite it and lose all data? y/n\n")
        
            while True and not continueSetup:
                if choice=="y":
                    continueSetup=True
                    break 
                else:
                    continueSetup=False
                    break
        else:
            continueSetup=False
        if continueSetup:
            try:
                self.db.close()
                if os.path.exists(self.connectionString):
                    os.remove(self.connectionString)
                
            except:
                pass

            print("Setting up database")
            self.db= Database(self.connectionString)
            self._setupTables()
        elif not compatibleDb and not continueSetup:
           print("\nYou wont be able to use this program, by not having a compatible database and not overwriting the existing one.")
           exit() 
        elif counter==0:
            print("\nStarting with a clean database...")
            try:
                self.db.close()
                if os.path.exists(self.connectionString):
                    os.remove(self.connectionString)
                
            except:
                pass

            print("Setting up database")
            self.db= Database(self.connectionString)
            self._setupTables()
        elif counter!=0:
            print("\nProgram is now using a seamingly compatible database")    
        
        pass

    def _setupTables(self):
        print("Setting up client table")
        self.db.executeNonResultQuery("""
            CREATE TABLE "client" (
                "id"	INTEGER,
                "fullname"	TEXT,
                "emailAddress"	TEXT UNIQUE,
                "address"	TEXT,
                "mobilePhoneNumber"	TEXT,
                "createdBy"	INTEGER,
                "created"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)
        
        ConsoleUtility.rewriteLastLine("Setting up logging table")
        self.db.executeNonResultQuery("""
            CREATE TABLE "logging" (
                "id"	INTEGER,
                "username"	TEXT,
                "userId"	INTEGER,
                "date"	TEXT,
                "time"	TEXT,
                "description"	TEXT,
                "additionalInfo"	TEXT,
                "suspicious"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)

        ConsoleUtility.rewriteLastLine("Setting up user table")
        self.db.executeNonResultQuery("""
            CREATE TABLE "user" (
                "id"	INTEGER,
                "fullname"	TEXT,
                "username"	TEXT UNIQUE,
                "role"	INTEGER,
                "passwordHash"	TEXT,
                "createdBy"	INTEGER,
                "created"	TEXT,
                "emailaddress"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """)
        print("Setup done                 ")
    def checkUser(self,username:str,password:str)->User: 
        args=[EncryptionProvider.getGlobalEncriptifier().encrypt(username), EncryptionProvider.getGlobalEncriptifier().encrypt(password)]
        rows= self.db.executeResultingQuery("""
            SELECT user.username, user.passwordHash, id,fullname,role,createdBy,created FROM "user" where user.username=? and user.passwordHash=? ;
        """,args)
        if len(rows)!=0 and rows[0][0]==args[0] and rows[0][1]==args[1]:
            if Constants.getRoleById(rows[0][4])=="advisor":
                return Advisor(EncryptionProvider.instance.decrypt(rows[0][3]),Username(EncryptionProvider.instance.decrypt(rows[0][0])),Password(EncryptionProvider.instance.decrypt(rows[0][1])),id=rows[0][2])
            elif Constants.getRoleById(rows[0][4])=="systemadmin":
                return SystemAdmin(EncryptionProvider.instance.decrypt(rows[0][3]),Username(EncryptionProvider.instance.decrypt(rows[0][0])),Password(EncryptionProvider.instance.decrypt(rows[0][1])),id=rows[0][2])
        return None

    

    def prepareinsert(self,mydict):
        query = "INSERT INTO {0} ({1}) VALUES ({2});"
        d = dict(mydict)
        table = d.pop('table')
        d.pop("id")
        columns = ','.join(d.keys())
        placeholders = ','.join(['?'] * len(d))
        values = d.values()
        return (query.format(table, columns, placeholders), values)
    
    def insert(self,completedict:dict, name:str):
        completedict.update({"table":name})
        (query, params)=self.prepareinsert(completedict)
        return self.db.executeNonResultQuery(query,list(params))

    def insertUserNew(self, newUser:User, role:str, createdBy:int,created:str):
        completeDict=dict(newUser.__dict__)
        completeDict.update({"role":role,"createdBy":createdBy,"created":created})
        return self.insert(completeDict,"user")

    def insertClientNew(self, newUser:User, createdBy:int,created:str):
        completeDict=dict(newUser.__dict__)
        completeDict.update({"createdBy":createdBy,"created":created})
        return self.insert(completeDict,"user")

    def select(self,object:any,name:str=None)->list:
        query="SELECT * FROM {0}".format(object.__name__ if name==None else name)
        return self.db.executeResultingQuery(query)

    def prepareUpdate(self,mydict):
        query = "UPDATE {0} SET {1} WHERE id=?;"
        d = dict(mydict)
        table = d.pop('table')
        id=d.pop("id")
        columns = '= ?, '.join(d.keys())+"=? "
        values = d.values()
        return (query.format(table, columns,id), values)

    # def updateUser(self, newUser:User, role:str, createdBy:int,created:str):
    #     completeDict=dict(newUser.__dict__)
    #     completeDict.update({"role":role,"createdBy":createdBy,"created":created})
    #     return self.insert(completeDict,"user")

    def update(self,object:any):
        name=type(object).__name__
        dictionary=dict(object.__dict__)
        dictionary.update({"table":name})
        (query, params)=self.prepareUpdate(dictionary)
        try:
            args=list(params)
            args.append(object.id)
            self.db.executeNonResultQuery(query,args)
            return True
        except Exception as e:
            return False

    def delete(self,object)->bool:
        name=type(object).__name__
        dictionary=dict(object.__dict__)
        id=-1
        if "id" in dictionary:
            id=dictionary["id"]
            if id>0:
                query="DELETE FROM {0} WHERE id=?".format(name)
                try:
                    self.db.executeNonResultQuery(query,[id])
                except:
                    return False
                return True
            return False
        else:
            return False
    # def fUser(self, newUser:User, role:str, createdBy:int,created:str):
    #     args=[newUser.fullName,newUser.username,role,newUser.passwordHash,createdBy,created]
    #     query = "INSERT INTO user (fullname, username, role, passwordHash, createdBy, created) VALUES (?, ?, ?, ?, ?, ?)"
         
    #     rowsAffected=self.db.executeQuery(query,args)
    #     #straks ff checken wat er in rowsaffected zit joe
    #     if rowsAffected==1:
    #         return newUser
    #     else:
    #         return None
class DatabaseWrapperProvider:
    @staticmethod
    def getGlobalDbWrapper()->DatabaseWrapper:
        return DatabaseWrapperProvider.instance
    @staticmethod
    def setGlobalDbWrapper(value):
        DatabaseWrapperProvider.instance:DatabaseWrapper=value