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
        
def getTableData(tableName, whereClause=''):
    qryStr = f'Select * from {tableName}'
    cursor = DB.connection.cursor()
    cursor.execute(' '.join([qryStr, whereClause]))
    columnNames = [column[0] for column in cursor.description]
    rowList = [row for row in cursor]
    cursor.close()
    return columnNames, rowList

def buildTree(columnNames, rows, parent, scrollBar, columnWidth=150):
    T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=6, padding=5, yscrollcommand=scrollBar.set)
    for i in range(len(columnNames)):
        T.column('# '+str(i+1), anchor=tk.CENTER, width=columnWidth)
        T.heading('# '+str(i+1), text=columnNames[i])
    for row in [list(r) for r in rows]:
        T.insert('', tk.END, text=row, values=row)
    return T 

DB = DatabaseManager()

def getProjectData(employeeNum):
    '''get Project data from the SQL database'''

    SQLQuery = f'''SELECT ProjectID, ProjectName, HoursWorked
            FROM ProjectHrsWorkedEmpNum_View 
            WHERE EmployeeNum = {employeeNum} 
            ORDER BY ProjectName'''
    fieldList = ['ProjectID', 'ProjectName', 'HoursWorked']

    rowList = DB.query(SQLQuery)
    return fieldList, rowList

def showGUI():
    window = tk.Tk()
    window.title('Update Hours')
    employeeFields, employeeRows = getTableData('EmployeeName_View')

    employeeInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    employeeInfoFrm.pack(anchor='w')
    employeeLabel = tk.Label(master=employeeInfoFrm, text='Employee:')
    employeeLabel.grid(column=0,row=0, sticky='w')
    
    employeeSb = tk.Scrollbar(master=employeeInfoFrm, orient='vertical')
    employeeSb.grid(column=1,row=1,sticky='ns')
    employeeTree = buildTree(employeeFields, employeeRows, employeeInfoFrm, employeeSb)
    employeeSb.config(command=employeeTree.yview)
    employeeTree.grid(column=0,row=1)

    def employeeTreeHandler(e = None):
        try:
            employeeNum = employeeTree.item(employeeTree.focus())['values'][0]
            projectFields, projectRows = getTableData('ProjectHrsWorkedEmpNum_View', f'WHERE EmployeeNum = {employeeNum}')
            projectRows = [list(row) for row in projectRows]
            projectTree.delete(*projectTree.get_children())
            for row in projectRows:
                projectTree.insert('', tk.END, text=row[0], values=row)
        except Exception as e:
            print(e)
    employeeTree.bind('<ButtonRelease-1>', employeeTreeHandler)

    projectFields, projectRows = getTableData('ProjectHrsWorkedEmpNum_View')

    projectInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    projectInfoFrm.pack(anchor='w')
    projectLabel = tk.Label(master=projectInfoFrm, text='Project:')
    projectLabel.grid(column=0,row=0, sticky='w')
    
    projectSb = tk.Scrollbar(master=projectInfoFrm, orient='vertical')
    projectSb.grid(column=1,row=1,sticky='ns')
    projectTree = buildTree(projectFields[:3], [], projectInfoFrm, projectSb)
    projectSb.config(command=projectTree.yview)
    projectTree.grid(column=0,row=1)

    def projectTreeHandler(e=None):
        hoursWorkedTxt.delete('1.0', tk.END)
        hoursWorkedTxt.insert(tk.END, projectTree.item(projectTree.focus())['values'][2])
    
    projectTree.bind('<ButtonRelease-1>', projectTreeHandler)

    hoursWorkedInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    hoursWorkedInfoFrm.pack(anchor='w')

    hoursWorkedLbl = tk.Label(master=hoursWorkedInfoFrm,text='Hours Worked: ')
    hoursWorkedLbl.grid(column=0,row=0)

    hoursWorkedTxt = tk.Text(master=hoursWorkedInfoFrm,width=15, height=1)
    hoursWorkedTxt.grid(column=1,row=0, sticky='w')

    def updateDatabase(e=None):
        projectID = projectTree.item(projectTree.focus())['values'][0]
        employeeNum = employeeTree.item(employeeTree.focus())['values'][0]
        newHoursWorked = hoursWorkedTxt.get('1.0', 'end')
        newHoursWorked = float(newHoursWorked[:len(newHoursWorked)-1])
        cmdStr = f'execute UpdateAssignment {projectID}, {employeeNum}, {newHoursWorked}'
        DB.command(cmdStr)
        employeeTreeHandler()


    updateBtn = tk.Button(master=hoursWorkedInfoFrm, text='Update', command=updateDatabase)
    updateBtn.grid(column=2,row=0)

    window.mainloop()

showGUI()