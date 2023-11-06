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

def getTrainerData():
    '''get Trainer data from the SQL database'''

    SQLQuery = '''SELECT TrainerID, LastName, FirstName 
        FROM  TrainerName_View 
        ORDER BY LastName, FirstName'''

    fieldList = ['TrainerID', 'LastName', 'FirstName']

    rowList = DB.query(SQLQuery)
    return fieldList, rowList

def getActivityData(TrainerID=100):
    '''get Activity data from the SQL database'''

    SQLQuery = f'''SELECT ActivityName, LevelType, StartDate, StartTime, EndTime 
        FROM  TrainerActivity_View
        WHERE TrainerID = {TrainerID}'''
    fieldList = ['ActivityName', 'LevelType', 'StartDate', 'StartTime', 'EndTime']

    rowList = DB.query(SQLQuery)
    return fieldList, rowList

def getQualificationData(TrainerID=100):
    '''get Qualification data from the SQL database'''

    SQLQuery = f'''SELECT ActivityName, LevelType, ApprovalDate 
        FROM  TrainerQualification_View
        WHERE TrainerID = {TrainerID}'''
    fieldList = ['ActivityName', 'LevelType', 'ApprovalDate']

    rowList = DB.query(SQLQuery)
    return fieldList, rowList

def showGUI():
    window = tk.Tk()
    window.title('Trainers')

    TrainerFields, TrainerRows = getTrainerData()

    TrainerInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    TrainerInfoFrm.pack(anchor='w')
    TrainerLabel = tk.Label(master=TrainerInfoFrm, text='Trainer:')
    TrainerLabel.grid(column=0,row=0, sticky='w')
    
    TrainerSb = tk.Scrollbar(master=TrainerInfoFrm, orient='vertical')
    TrainerSb.grid(column=1,row=1,sticky='ns')
    TrainerTree = ttk.Treeview(master=TrainerInfoFrm, columns=TrainerFields, show='headings', height=6, padding=5, yscrollcommand=TrainerSb.set)
    TrainerSb.config(command=TrainerTree.yview)

    TrainerTree.column('# 1', anchor=tk.CENTER, width=100)
    TrainerTree.heading('# 1', text='ID')
    TrainerTree.column('# 2', anchor=tk.CENTER, width=200)
    TrainerTree.heading('# 2', text='LastName')
    TrainerTree.column('# 3', anchor=tk.CENTER, width=200)
    TrainerTree.heading('# 3', text='FirstName')
    TrainerTree.grid(column=0,row=1)

    for row in TrainerRows:
        TrainerTree.insert('', tk.END, text=row[0], values=row)
    
    BtnFrm = tk.Frame(master=window, relief=tk.GROOVE, pady=10, width=500)
    BtnFrm.pack()

    def QualificationBtnHandler(e = None):
        TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
        LastName = TrainerTree.item(TrainerTree.focus())['values'][1]
        FirstName = TrainerTree.item(TrainerTree.focus())['values'][2]
        QualificationFields, QualificationRows = getQualificationData(TrainerID)
        win = tk.Tk()
        win.title(f"{FirstName} {LastName}\'s Qualifications")

        QualificationInfoFrm = tk.Frame(master=win, relief=tk.GROOVE, padx=50, pady=10, width=500)
        QualificationInfoFrm.pack(anchor='w')
        QualificationLabel = tk.Label(master=QualificationInfoFrm, text='Qualifications:', width=13)
        QualificationLabel.grid(column=0,row=0, sticky='w')

        QualificationSb = tk.Scrollbar(master=QualificationInfoFrm, orient='vertical')
        QualificationSb.grid(column=1,row=1,sticky='ns')
        QualificationTree = ttk.Treeview(master=QualificationInfoFrm, columns=QualificationFields, show='headings', height=6, padding=5, yscrollcommand=QualificationSb.set)
        QualificationSb.config(command=QualificationTree.yview)

        QualificationTree.column('# 1', anchor=tk.CENTER, width=100)
        QualificationTree.heading('# 1', text='ActivityName')
        QualificationTree.column('# 2', anchor=tk.CENTER, width=200)
        QualificationTree.heading('# 2', text='ActivityLevel')
        QualificationTree.column('# 3', anchor=tk.CENTER, width=200)
        QualificationTree.heading('# 3', text='ApprovalDate')
        QualificationTree.grid(column=0,row=1)
        for row in QualificationRows:
            QualificationTree.insert('', tk.END, text=row[0], values=row)

    QualificationBtn = tk.Button(master=BtnFrm, text='Show Qualifications', command=QualificationBtnHandler)
    QualificationBtn.grid(column=0,row=0)

    def ActivityBtnHandler(e = None):
        TrainerID = TrainerTree.item(TrainerTree.focus())['values'][0]
        LastName = TrainerTree.item(TrainerTree.focus())['values'][1]
        FirstName = TrainerTree.item(TrainerTree.focus())['values'][2]
        ActivityFields, ActivityRows = getActivityData(TrainerID)

        win = tk.Tk()
        win.title(f'{FirstName} {LastName}\'s Activities')

        ActivityInfoFrm = tk.Frame(master=win, relief=tk.GROOVE, padx=50, pady=10)
        ActivityInfoFrm.pack(anchor='w')
        ActivityLabel = tk.Label(master=ActivityInfoFrm, text='Activities:')
        ActivityLabel.grid(column=0,row=0, sticky='w')

        ActivitySb = tk.Scrollbar(master=ActivityInfoFrm, orient='vertical')
        ActivitySb.grid(column=1,row=1,sticky='ns')
        ActivityTree = ttk.Treeview(master=ActivityInfoFrm, columns=ActivityFields, show='headings', height=6, padding=5, yscrollcommand=ActivitySb.set)
        ActivitySb.config(command=ActivityTree.yview)

        ActivityTree.column('# 1', anchor=tk.CENTER, width=100)
        ActivityTree.heading('# 1', text='ActivityName')
        ActivityTree.column('# 2', anchor=tk.CENTER, width=100)
        ActivityTree.heading('# 2', text='ActivityLevel')
        ActivityTree.column('# 3', anchor=tk.CENTER, width=100)
        ActivityTree.heading('# 3', text='StartDate')
        ActivityTree.column('# 4', anchor=tk.CENTER, width=100)
        ActivityTree.heading('# 4', text='StartTime')
        ActivityTree.column('# 5', anchor=tk.CENTER, width=100)
        ActivityTree.heading('# 5', text='EndTime')
        ActivityTree.grid(column=0,row=1)

        for row in ActivityRows:
            ActivityTree.insert('', tk.END, text=row[0], values=row)

    ActivityBtn = tk.Button(master=BtnFrm, text='Show Activities', command=ActivityBtnHandler)
    ActivityBtn.grid(column=1,row=0)

    window.mainloop()
showGUI()