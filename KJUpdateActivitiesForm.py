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
    
    BtnFrm = tk.Frame(master=window, relief=tk.GROOVE, pady=10, width=500)
    BtnFrm.pack()

    def QualificationBtnHandler(e = None):
        try:
            TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
            LastName = TrainerTree.item(TrainerTree.focus())['values'][1]
            FirstName = TrainerTree.item(TrainerTree.focus())['values'][2]

            win = GUI(f"{FirstName} {LastName}\'s Qualifications")
            QualificationInfoFrm = tk.Frame(master=win.window, relief=tk.GROOVE, padx=50, pady=10, width=500)
            QualificationInfoFrm.pack(anchor='w')
            tk.Label(master=QualificationInfoFrm, text='Qualifications:', width=13).grid(column=0,row=0, sticky='w')
            QualificationSb = tk.Scrollbar(master=QualificationInfoFrm, orient='vertical')
            QualificationSb.grid(column=1,row=1,sticky='ns')
            QualificationTableData = getTableData(tableName='TrainerQualification_View', where=f'TrainerID = {TrainerID}', columns='LevelType, ActivityName, ApprovalDate')
            QualificationTree = buildTree(QualificationTableData.columns, QualificationTableData.rows, QualificationInfoFrm, QualificationSb)
            QualificationSb.config(command=QualificationTree.yview)
            QualificationTree.grid(column=0,row=1)
        except Exception as e:
            print(e)

    ttk.Button(master=BtnFrm, text='Show Trainer Qualifications', command=QualificationBtnHandler).grid(column=0,row=0)

    def ActivityBtnHandler(e = None):
        try:
            TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
            LastName = TrainerTree.item(TrainerTree.focus())['values'][1]
            FirstName = TrainerTree.item(TrainerTree.focus())['values'][2]

            win = GUI(f'{FirstName} {LastName}\'s Activities')
            ActivityInfoFrm = tk.Frame(master=win.window, relief=tk.GROOVE, padx=50, pady=10)
            ActivityInfoFrm.pack(anchor='w')
            ttk.Label(master=ActivityInfoFrm, text='Activities:').grid(column=0,row=0, sticky='w')
            ActivitySb = tk.Scrollbar(master=ActivityInfoFrm, orient='vertical')
            ActivitySb.grid(column=1,row=1,sticky='ns')
            ActivityTableData = getTableData(tableName='TrainerActivity_View', where=f'TrainerID = {TrainerID}', columns='LevelType, ActivityName, StartDate, StartTime, EndTime')
            ActivityTree = buildTree(columnNames=ActivityTableData.columns, rows=ActivityTableData.rows, parent=ActivityInfoFrm, scrollBar=ActivitySb)
            ActivitySb.config(command=ActivityTree.yview)
            ActivityTree.grid(column=0,row=1)
        except Exception as e:
            print(e)

    ttk.Button(master=BtnFrm, text='Show Trainer Activities', command=ActivityBtnHandler).grid(column=1,row=0)

    def approvedActivityBtnHandler(e = None):
        try:
            win = GUI('Approved Activites')

            approvedActivityInfoFrm = tk.Frame(master=win.window, relief=tk.GROOVE, padx=50, pady=10)
            approvedActivityInfoFrm.pack(anchor='w')
            ttk.Label(master=approvedActivityInfoFrm, text='Approved Activities:').grid(column=0, row=0, sticky='w')
            approvedActivitySb = ttk.Scrollbar(master=approvedActivityInfoFrm, orient='vertical')
            approvedActivitySb.grid(column=1, row=1, sticky='ns')
            approvedActivityTableData = getTableData('ApprovedActivity_View')
            approvedActivityTree = buildTree(approvedActivityTableData.columns, approvedActivityTableData.rows, approvedActivityInfoFrm, approvedActivitySb)
            approvedActivitySb.config(command=approvedActivityTree.yview)
            approvedActivityTree.grid(column=0, row=1)
        except Exception as e:
            print(e)

    ttk.Button(master=BtnFrm, text='Show Approved Activities', command=approvedActivityBtnHandler).grid(column=2,row=0)

    window.mainloop()
showGUI()