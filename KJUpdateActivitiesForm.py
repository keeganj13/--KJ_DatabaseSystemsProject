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

def getTableData(tableName, whereClause=''):
    qryStr = f'Select * from {tableName}'
    cursor = DB.connection.cursor()
    cursor.execute(' '.join([qryStr, whereClause]))
    columnNames = [column[0] for column in cursor.description]
    rowList = [row for row in cursor]
    cursor.close()
    return columnNames, rowList

def buildTree(columnNames, rows, parent, scrollBar, columnWidth=100):
    T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=6, padding=5, yscrollcommand=scrollBar.set)
    for i in range(len(columnNames)):
        T.column('# '+str(i+1), anchor=tk.CENTER, width=columnWidth)
        T.heading('# '+str(i+1), text=columnNames[i])
    for row in [list(r) for r in rows]:
        T.insert('', tk.END, text=row, values=row)
    return T 

def showGUI():
    window = tk.Tk()
    window.title('Trainers')

    TrainerFields, TrainerRows = getTableData('TrainerName_View')

    TrainerInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    TrainerInfoFrm.pack(anchor='w')
    TrainerLabel = tk.Label(master=TrainerInfoFrm, text='Trainer:')
    TrainerLabel.grid(column=0,row=0, sticky='w')
    
    TrainerSb = tk.Scrollbar(master=TrainerInfoFrm, orient='vertical')
    TrainerSb.grid(column=1,row=1,sticky='ns')
    TrainerTree = buildTree(TrainerFields, TrainerRows, TrainerInfoFrm, TrainerSb)
    TrainerTree.grid(column=0,row=1)
    TrainerSb.config(command=TrainerTree.yview)
    
    BtnFrm = tk.Frame(master=window, relief=tk.GROOVE, pady=10, width=500)
    BtnFrm.pack()

    def QualificationBtnHandler(e = None):
        TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
        LastName = TrainerTree.item(TrainerTree.focus())['values'][1]
        FirstName = TrainerTree.item(TrainerTree.focus())['values'][2]
        QualificationFields, QualificationRows = getTableData('TrainerQualification_View', f'WHERE TrainerID = {TrainerID}')
        QualificationRows = [row[3:] for row in QualificationRows]
        QualificationFields = QualificationFields[3:]
        win = tk.Tk()
        win.title(f"{FirstName} {LastName}\'s Qualifications")

        QualificationInfoFrm = tk.Frame(master=win, relief=tk.GROOVE, padx=50, pady=10, width=500)
        QualificationInfoFrm.pack(anchor='w')
        QualificationLabel = tk.Label(master=QualificationInfoFrm, text='Qualifications:', width=13)
        QualificationLabel.grid(column=0,row=0, sticky='w')

        QualificationSb = tk.Scrollbar(master=QualificationInfoFrm, orient='vertical')
        QualificationSb.grid(column=1,row=1,sticky='ns')
        QualificationTree = buildTree(QualificationFields, QualificationRows, QualificationInfoFrm, QualificationSb)
        QualificationSb.config(command=QualificationTree.yview)
        QualificationTree.grid(column=0,row=1)

    QualificationBtn = tk.Button(master=BtnFrm, text='Show Qualifications', command=QualificationBtnHandler)
    QualificationBtn.grid(column=0,row=0)

    def ActivityBtnHandler(e = None):
        TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
        LastName = TrainerTree.item(TrainerTree.focus())['values'][1]
        FirstName = TrainerTree.item(TrainerTree.focus())['values'][2]
        ActivityFields, ActivityRows = getTableData('TrainerActivity_View', f'WHERE TrainerID = {TrainerID}')
        ActivityFields = ActivityFields[3:]
        ActivityRows = [row[3:] for row in ActivityRows]
        win = tk.Tk()
        win.title(f'{FirstName} {LastName}\'s Activities')

        ActivityInfoFrm = tk.Frame(master=win, relief=tk.GROOVE, padx=50, pady=10)
        ActivityInfoFrm.pack(anchor='w')
        ActivityLabel = tk.Label(master=ActivityInfoFrm, text='Activities:')
        ActivityLabel.grid(column=0,row=0, sticky='w')

        ActivitySb = tk.Scrollbar(master=ActivityInfoFrm, orient='vertical')
        ActivitySb.grid(column=1,row=1,sticky='ns')
        ActivityTree = buildTree(parent=ActivityInfoFrm, rows=ActivityRows, columnNames=ActivityFields, scrollBar=ActivitySb)
        ActivitySb.config(command=ActivityTree.yview)
        ActivityTree.grid(column=0,row=1)

    ActivityBtn = tk.Button(master=BtnFrm, text='Show Activities', command=ActivityBtnHandler)
    ActivityBtn.grid(column=1,row=0)

    window.mainloop()
showGUI()