
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
        cursor.execute(SQLQuery)
        out = cursor.fetchall()
        cursor.commit()
        return [list(row) for row in out]

DB = DatabaseManager()

def readFile(fileName):
    tmpFile = open(fileName, 'r')
    return tmpFile.readlines()

createProjectTablesScript = ' '.join([row.strip() for row in readFile('KJCreateTables.sql')]).split(';')
# print(createProjectTablesScript)
for line in createProjectTablesScript:
    DB.query(line)
    # print(line,end='')

createProjectViewsScript = [line.strip() for line in readFile('KJCreateViews.sql')]
index=0
for line in createProjectViewsScript:
    if 'DROP' in line:
        DB.query(line)
        # print(line)
        index+=1
    else:
        break

while index < len(createProjectViewsScript):
    if 'CREATE' in createProjectViewsScript[index]:
        j=1
        while index + j < len(createProjectViewsScript) and 'CREATE' not in createProjectViewsScript[index+j]:
            j += 1
        DB.query(' '.join(createProjectViewsScript[index:index+j]))
        # print(' '.join(createProjectViewsScript[index:index+j]))
        index += j
    else:
        index += 1

createTablesScript = [line.strip() for line in readFile('SQLCreateTablesAndData.sql')]
DB.query(' '.join(createTablesScript))

DB.query('DROP VIEW IF EXISTS EmployeeName_View')
# print('DROP VIEW IF EXISTS EmployeeName_View')
DB.query('DROP VIEW IF EXISTS ProjectHrsWorkedEmpNum_View')
# print('DROP VIEW IF EXISTS ProjectHrsWorkedEmpNum_View')

employeeNameViewScript = [line.strip() for line in readFile('EmployeeName_View.sql')]
DB.query(' '.join(employeeNameViewScript))
# print(' '.join(employeeNameViewScript))
projectEmployeeViewScript = [line.strip() for line in readFile('ProjectHrsWorkedEmpNum_View.sql')]
DB.query(' '.join(projectEmployeeViewScript))
# print(' '.join(projectEmployeeViewScript))
