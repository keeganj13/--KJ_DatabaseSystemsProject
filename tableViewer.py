import pyodbc
import tkinter as tk
from tkinter import ttk

class DatabaseManager:
    '''An object that serves as a connection to a database'''
    def __init__(self, server='', db='', uid='', pwd=''):
        connectionString = 'DRIVER={SQL Server};' + f'SERVER={server};DATABASE={db};UID={uid};PWD={pwd}'
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
        cursor.close()
        return tableNames
    
    def getViewNames(self):
        cursor = self.connection.cursor()
        viewNames = [(item[2]) for item in cursor.tables(tableType='VIEW') if 'dbo' in item]
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

class GUI:
    def __init__(self, title='Untitled Window'):
        self.window = tk.Tk()
        self.window.title(title)
    def show(self):
        self.window.mainloop()

def buildTree(columnNames=[], rows=[], parent= None, scrollBar=None, columnWidth=130, customHeight=6, customPadding=5):
    '''returns a Tkinter Treeview Object based on the inputs'''
    if parent == None:
        print('Tree object needs a parent object')
        return None
    sbcommand = None
    if scrollBar is not None:
        sbcommand = scrollBar.set
    if type(columnNames) == type(''):
        columnNames = columnNames.split(', ')
    elif type(columnNames) not in [type(()), type([])]:
        columnNames = ['']
    else:
        columnNames = list(columnNames)
    if type(customHeight) not in [type(0), type('0'), type(0.0)]:
        customHeight = 6
    else:
        customHeight = int(eval(str(customHeight)))
    if type(customPadding) not in [type(0), type('0'), type(0.0)]:
        customPadding = 5
    else:
        customPadding = int(eval(str(customPadding)))

    try:
        T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=customHeight, padding=customPadding, yscrollcommand=sbcommand)
        for i in range(len(columnNames)):
            T.column('# '+str(i+1), anchor=tk.CENTER, width=columnWidth)
            T.heading('# '+str(i+1), text=columnNames[i])
        for row in [list(r) for r in rows]:
            T.insert('', tk.END, text=row, values=row)
        return T
    except Exception as e:
        print(e)
        return None 

def getTableData(tableName='', columns='*', where='', order=''):
    '''returns a TableData object with the result data from the inputted SQL query'''
    try:
        if type(columns) == type([]):
            columns = ', '.join(columns)
    except Exception as e:
        return e
    try:
        if len(where) > 0 and 'WHERE' not in where.upper(): where = 'WHERE ' + where
        if len(order) > 0 and 'ORDER BY' not in order.upper(): order = 'ORDER BY ' + order
    except Exception as e:
        return e

    qryStr = f'Select {columns} from {tableName} {where} {order}'
    qryResultData = DB.query(qryStr)
    columns, rows = qryResultData.columns, qryResultData.rows
    return TableData(columns, rows)

DB = DatabaseManager(
    server='68.44.168.125', 
    db='KeeganDB',
    uid='Keegan', 
    pwd='svu090') 

def main():
    mainPopup = GUI('Database Manager')

    tablesInfoFrm = tk.Frame(master=mainPopup.window, padx=10,pady=10)
    tablesInfoFrm.pack()
    tablesLbl = tk.Label(master=tablesInfoFrm, text='Tables:')
    tablesLbl.grid(column=0,row=0,sticky='w')
    tablesSb = tk.Scrollbar(master=tablesInfoFrm, orient='vertical')
    tablesSb.grid(column=1,row=1,sticky='ns')
    tableNames = [[item] for item in DB.getTableNames()]
    tablesTree = buildTree(['Table Name'], tableNames, tablesInfoFrm, tablesSb, 200)
    tablesTree.grid(column=0,row=1)
    tablesSb.config(command=tablesTree.yview)

    def showTableBtnHandler(e = None):
        try:
            curTableName = tablesTree.item(tablesTree.focus())["values"][0]
            curTablePopup = GUI(f'{curTableName} Info')
            tableInfoFrm = tk.Frame(master=curTablePopup.window, padx=10,pady=10)
            tableInfoFrm.pack()
            curTableData = getTableData(curTableName)
            tableSb = tk.Scrollbar(master=tableInfoFrm, orient='vertical')
            tableSb.grid(column=1,row=1,sticky='ns')
            tableTree = buildTree(curTableData.columns, curTableData.rows, tableInfoFrm, tableSb, customHeight=len(curTableData.rows) // 2+1)
            tableTree.grid(column=0,row=1)
            tableSb.config(command=tableTree.yview)
            curTablePopup.show()
        except Exception as e:
            print(e)
        
    tk.Button(master=tablesInfoFrm, text='Show Table Info', command=showTableBtnHandler).grid(column=0,row=2)

    viewsInfoFrm = tk.Frame(master=mainPopup.window, padx=10,pady=10)
    viewsInfoFrm.pack()
    ttk.Label(master=viewsInfoFrm, text='Views:').grid(column=0,row=0,sticky='w')
    viewsSb = tk.Scrollbar(master=viewsInfoFrm, orient='vertical')
    viewsSb.grid(column=1,row=1,sticky='ns')
    viewNames = [[item] for item in DB.getViewNames()]
    viewsTree = buildTree(['View Name'], viewNames, viewsInfoFrm, viewsSb, 200)
    viewsTree.grid(column=0,row=1)
    viewsSb.config(command=viewsTree.yview)

    def showViewBtnHandler(e = None):
        try:
            curViewName = viewsTree.item(viewsTree.focus())["values"][0]
            curViewPopup = GUI(f'{curViewName} Info')
            viewInfoFrm = tk.Frame(master=curViewPopup.window, padx=10,pady=10)
            viewInfoFrm.pack()
            curViewData = getTableData(curViewName)
            viewSB = tk.Scrollbar(master=viewInfoFrm, orient='vertical')
            viewSB.grid(column=1,row=1,sticky='ns')
            viewTree = buildTree(curViewData.columns, curViewData.rows, viewInfoFrm, viewSB, customHeight=len(curViewData.rows) // 2+1)
            viewTree.grid(column=0,row=1)
            viewSB.config(command=viewTree.yview)
            curViewPopup.show()
        except Exception as e:
            print(e)
        
    tk.Button(master=viewsInfoFrm, text='Show View Info', command=showViewBtnHandler).grid(column=0,row=2)

    mainPopup.show()
main()

