from data.databaseWrapper import DatabaseWrapper, DatabaseWrapperProvider
from datetime import datetime
import os
import zipfile

class Backup:
    @staticmethod
    def doBackup():
        DatabaseWrapperProvider.instance.db.close()
        DatabaseWrapperProvider.instance=DatabaseWrapper("appDB.db")
        DatabaseWrapperProvider.instance.initializeDatabase()
        timestamp=datetime.now().strftime("%d%m%Y%H%M%S")
        zipfile.ZipFile(f'backup{timestamp}.zip', mode='w').write("appDB.db")
        print(f"Backup done see backup{timestamp}.zip")