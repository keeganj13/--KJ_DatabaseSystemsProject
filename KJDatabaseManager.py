
import pyodbc
import tkinter as tk
from tkinter import ttk

class DatabaseManager:
    '''An object that serves as a connection to a database'''
    def __init__(self, server='', db='', uid='', pwd=''):
        connectionString = 'DRIVER={SQL Server};' + ''.join([server,db,uid,pwd])
        self.connection  = pyodbc.connect(connectionString)

    def query(self, SQLQuery=''):
        '''returns a TableData object with the result data from querying SQLQuery'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(SQLQuery)
            columns, rows = [item[0] for item in cursor.description], [list(row) for row in cursor.fetchall()]
            cursor.commit()
            cursor.close()
            return TableData(columns, rows)
        except Exception as e:
            return e, SQLQuery
    
    def command(self, SQLCommand):
        '''executes SQLCommand without returning data'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(SQLCommand)
            cursor.commit()
            cursor.close()
            return 'Command success.'
        except Exception as e:
            return e, SQLCommand
    
    def getTableNames(self):
        cursor = self.connection.cursor()
        tableNames = [(item[2]) for item in cursor.tables(tableType='TABLE') if 'dbo' in item]
        cursor.commit()
        cursor.close()
        return tableNames
    
    def getViewNames(self):
        cursor = self.connection.cursor()
        viewNames = [(item[2]) for item in cursor.tables(tableType='VIEW') if 'dbo' in item]
        cursor.commit()
        cursor.close()
        return viewNames

class TableData:
    '''An object with lists of row and column data from a table'''
    def __init__(self, columns=[], rows=[]):
        '''initializes a TableData object'''
        if type(columns) not in [type(()), type([])]:
            columns = []
        if type(rows) not in [type(()), type([])]:
            rows = []
        self.columns = list(columns)
        self.rows = list(rows) 
        
DB = DatabaseManager(
    server='SERVER=68.44.168.125;', 
    db='DATABASE=KeeganDB;',
    uid='UID=Keegan;', 
    pwd='PWD=svu090') 

def readFile(fileName):
    try:
        fileData = open(fileName, 'r')
        return fileData.readlines()
    except Exception as e:
        return False, e

def runSQLFile(fileName):
    try:
        fileData = readFile(fileName)
        if type(fileData) != type(()): 
            SQLScript = ' '.join([row.strip() for row in readFile(fileName)]).split(';')
            for line in SQLScript: 
                if len(line) > 1: print(DB.command(line))
            print('SQL Script Completed.')
        else:
            print(fileData[1])
    except Exception as e:
        print(e)

# runSQLFile('CreateBookstoresDB_TablesScript - v3(1).sql')
runSQLFile('KJCreateTables.sql')
runSQLFile('KJCreateViews.sql')
# runSQLFile('SQLCreateTablesAndData.sql')
# runSQLFile('EmployeeName_View.sql')
# runSQLFile('ProjectHrsWorkedEmpNum_View.sql')
