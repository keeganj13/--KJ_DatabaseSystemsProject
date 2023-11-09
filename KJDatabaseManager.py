
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
            return e, SQLCommand

DB = DatabaseManager()

def readFile(fileName):
    tmpFile = open(fileName, 'r')
    return tmpFile.readlines()

def runSQLFile(fileName):
    SQLScript = ' '.join([row.strip() for row in readFile(fileName)]).split(';')
    for line in SQLScript: 
        if len(line) > 1: print(DB.command(line))
    print('SQL Script Completed.')

runSQLFile('CreateBookstoresDB_TablesScript - v3(1).sql')
# runSQLFile('KJCreateTables.sql')
# runSQLFile('KJCreateViews.sql')
# runSQLFile('SQLCreateTablesAndData.sql')
# runSQLFile('EmployeeName_View.sql')
# runSQLFile('ProjectHrsWorkedEmpNum_View.sql')
