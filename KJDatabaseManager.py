
import pyodbc
import tkinter as tk
from tkinter import ttk

class DatabaseManager:
    def __init__(self):
        self.connectionString = '''DRIVER={SQL Server};
            SERVER=68.44.168.125;
            DATABASE=KeeganDB;
            UID=Keegan;
            PWD=svu090'''
        self.connection  = pyodbc.connect(self.connectionString)
    def query(self, SQLQuery):
        cursor = self.connection.cursor()
        try:
            cursor.execute(SQLQuery)
            out = cursor.fetchall()
            return [list(row) for row in out]
        except Exception as e:
            return e
    
    def command(self, SQLCommand):
        cursor = self.connection.cursor()
        try:
            cursor.execute(SQLCommand)
            cursor.commit()
            return 'Command success.'
        except Exception as e:
            return e

DB = DatabaseManager()

def readFile(fileName):
    tmpFile = open(fileName, 'r')
    return tmpFile.readlines()

projTableScript = ' '.join([row.strip() for row in readFile('KJCreateTables.sql')]).split(';')
for i in range(len(projTableScript)):
    line = projTableScript[i]
    if len(line)> 1: print(DB.command(line))


projViewScript = ' '.join([row.strip() for row in readFile('KJCreateViews.sql')]).split(';')
for i in range(len(projViewScript)):
    line = projViewScript[i]
    if len(line)> 1: print(DB.command(line))


# tableScript = ' '.join([line.strip() for line in readFile('SQLCreateTablesAndData.sql')]).split(';')
# for line in tableScript:
#     if len(line)> 1: print(DB.command(line))

# employeeNameViewScript = ' '.join([line.strip() for line in readFile('EmployeeName_View.sql')]).split(';')
# for line in employeeNameViewScript:
#     if len(line)> 1: print(DB.command(line))
# projectEmployeeViewScript = ' '.join([line.strip() for line in readFile('ProjectHrsWorkedEmpNum_View.sql')]).split(';')
# for line in projectEmployeeViewScript:
#     if len(line)> 1: print(DB.command(line))
