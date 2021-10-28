import sqlite3

class Database:
    def __init__(self, connectionString=None):
        self.connection = None
        self.cursor = None
        if connectionString:
            self.connect(connectionString)
    def connect(self, connectionString):
        try:
            self.connection = sqlite3.connect(connectionString)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to the database")

    def close(self):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    def executeNonResultQuery(self,query,args=[]):
        cursor = self.connection.cursor()
        result= cursor.execute(query,args)
        self.connection.commit()
        return result
        
    def executeResultingQuery(self,query,args=[]):
        cursor = self.connection.cursor()
        result= cursor.execute(query,args)
        resultRows=result.fetchall()
        return resultRows