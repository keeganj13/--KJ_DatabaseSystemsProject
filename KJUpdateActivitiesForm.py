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
class GUI:
    def __init__(self, title='Window Title'):
        self.title = title
        self.window = tk.Tk()
        self.window.title(self.title)
    def show(self):
        self.window.mainloop()

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
    server='68.44.168.125',
    db='KeeganDB', 
    uid='Keegan',
    pwd='svu090')

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

def showGUI():
    window = tk.Tk()
    window.title('Trainers')

    TrainerTableData = getTableData('TrainerName_View')

    TrainerInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    TrainerInfoFrm.pack(anchor='w')
    ttk.Label(master=TrainerInfoFrm, text='Trainer:').grid(column=0,row=0, sticky='w')
    
    TrainerSb = tk.Scrollbar(master=TrainerInfoFrm, orient='vertical')
    TrainerSb.grid(column=1,row=1,sticky='ns')
    TrainerTree = buildTree(TrainerTableData.columns, TrainerTableData.rows, TrainerInfoFrm, TrainerSb)
    TrainerTree.grid(column=0,row=1)
    TrainerSb.config(command=TrainerTree.yview)
    
    ApprovedActivityInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    ApprovedActivityInfoFrm.pack(anchor='w')
    ttk.Label(master=ApprovedActivityInfoFrm, text='Qualifications:').grid(column=0, row=0, sticky='w')
    ApprovedActivitySb = ttk.Scrollbar(master=ApprovedActivityInfoFrm, orient='vertical')
    ApprovedActivitySb.grid(column=1, row=1, sticky='ns')
    ApprovedActivityTree = buildTree(['LevelType', 'ActivityName', 'ApprovalDate'], [], ApprovedActivityInfoFrm, ApprovedActivitySb)
    ApprovedActivitySb.config(command=ApprovedActivityTree.yview)
    ApprovedActivityTree.grid(column=0, row=1)

    updateApprovalDateFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    updateApprovalDateFrm.pack(anchor='w')
    tk.Label(master=updateApprovalDateFrm, text='Approval Date:').grid(column=0, row=0, sticky='w')
    updateEntry = tk.Entry(master=updateApprovalDateFrm, width=25, background='white')
    updateEntry.grid(column=1,row=0,padx=10)

    def TrainerTreeHandler(e=None):
        try:
            TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
            TrainerQualificationTableData = getTableData('TrainerQualification_View',where=f'TrainerID = {TrainerID}', columns='LevelType, ActivityName, ApprovalDate')
            ApprovedActivityTree.delete(*ApprovedActivityTree.get_children())
            for row in TrainerQualificationTableData.rows:
                ApprovedActivityTree.insert('', 'end', values=row, text=row)
        except Exception as err:
            print(err)
    
    def ApprovedActivityTreeHandler(e=None):
        try:
            ApprovalDate = ApprovedActivityTree.item(ApprovedActivityTree.focus())['values'][2]
            updateEntry.delete(0, 'end')
            updateEntry.insert(0, ApprovalDate)
        except Exception as err:
            print(err)
    
    def updateBtnHandler(e = None):
        try:
            ApprovalDate = updateEntry.get()
            TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
            LevelType = ApprovedActivityTree.item(ApprovedActivityTree.focus())['values'][0]
            ActivityName = ApprovedActivityTree.item(ApprovedActivityTree.focus())['values'][1]
            commandStr = f'execute UpdateApprovalDate {TrainerID}, {LevelType}, {ActivityName}, {ApprovalDate}'
            print(commandStr, 'h')
            DB.command(commandStr)
            TrainerTreeHandler(e)
        except Exception as err:
            print(err)

    tk.Button(master=updateApprovalDateFrm, text='Update Approval Date', command=updateBtnHandler).grid(column=2,row=0,padx=10)

    TrainerTree.bind('<ButtonRelease-1>', TrainerTreeHandler)
    ApprovedActivityTree.bind('<ButtonRelease-1>', ApprovedActivityTreeHandler)
    window.mainloop()
showGUI()