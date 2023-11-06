
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
        return [list(row) for row in cursor.fetchall()]

DB = DatabaseManager()

trainerInfo = DB.query('Select * From Trainer')

for line in trainerInfo:
    print(line)