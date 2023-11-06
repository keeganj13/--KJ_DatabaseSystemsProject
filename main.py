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
        
class GUI:
    def __init__(self, title='Window Title'):
        self.title = title
        self.window = tk.Tk()
        self.window.title(self.title)
    def show(self):
        self.window.mainloop()

def buildTree(columnNames, rows, parent, scrollBar, columnWidth=150):
    T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=6, padding=5, yscrollcommand=scrollBar.set)
    for i in range(len(columnNames)):
        T.column('# '+str(i+1), anchor=tk.CENTER, width=columnWidth)
        T.heading('# '+str(i+1), text=columnNames[i])
    for row in [list(r) for r in rows]:
        T.insert('', tk.END, text=row, values=row)
    return T  

DB = DatabaseManager()

mainPopup = GUI('Database Manager')

tablesInfoFrm = tk.Frame(master=mainPopup.window, padx=10,pady=10)
tablesInfoFrm.pack()

tablesLbl = tk.Label(master=tablesInfoFrm, text='Tables:')
tablesLbl.grid(column=0,row=0,sticky='w')

tablesSb = tk.Scrollbar(master=tablesInfoFrm, orient='vertical')
tablesSb.grid(column=1,row=1,sticky='ns')

cursor = DB.connection.cursor()
tablesRows = [[row[2]] for row in cursor.tables(tableType='TABLE') if 'dbo' in row[1]]

tablesTree = buildTree(['Table Name'], tablesRows, tablesInfoFrm, tablesSb, 200)
tablesTree.grid(column=0,row=1)
tablesSb.config(command=tablesTree.yview)

def getTableData(tableName, whereClause=''):
    qryStr = f'Select * from {tableName}'
    cursor = DB.connection.cursor()
    cursor.execute(' '.join([qryStr, whereClause]))
    columnNames = [column[0] for column in cursor.description]
    rowList = [row for row in cursor]
    cursor.close()
    return columnNames, rowList

def showBtnHandler(e = None):
    tableName = tablesTree.item(tablesTree.focus())["values"][0]
    tablePopup = GUI(f'{tableName} Info')
    tableInfoFrm = tk.Frame(master=tablePopup.window, padx=10,pady=10)
    tableInfoFrm.pack()
    tableColumns, tableRows = getTableData(tableName)

    tableSb = tk.Scrollbar(master=tableInfoFrm, orient='vertical')
    tableSb.grid(column=1,row=1,sticky='ns')
    tableTree = buildTree(tableColumns, tableRows, tableInfoFrm, tableSb)
    tableTree.grid(column=0,row=1)
    tableSb.config(command=tableTree.yview)
    
    tablePopup.show()
    
showBtn = tk.Button(master=tablesInfoFrm, text='Show Table Info', command=showBtnHandler)
showBtn.grid(column=0,row=2)

mainPopup.show()


