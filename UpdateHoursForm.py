######################## Python Library Importation ########################

import pyodbc # python library for connecting to databases
import tkinter as tk # python library for GUI creation
from tkinter import ttk # sublibrary for GUI creation

######################## Useful Class Creation ########################

class DatabaseManager:
    '''An object that serves as a connection to a database'''
    ######################## DatabaseManager Object Initiation ########################

    def __init__(self, server='', db='', uid='', pwd=''):
        connectionString = 'DRIVER={SQL Server};' + f'SERVER={server};DATABASE={db};UID={uid};PWD={pwd}'
        self.connection  = pyodbc.connect(connectionString)

    ######################## DatabaseManager Object Method Creation ########################

    def query(self, SQLQuery=''):
        '''returns a TableData object with the result data from querying SQLQuery'''
        cursor = self.connection.cursor()
        try:
            cursor.execute(SQLQuery)
            # the cursor.description is a list of descriptions of each column which are also lists
            # so the actual column name is the first item in the list for the description of that column
            # the cursor.fetchall() just gets all the result data from the SQL Query, which is put into rows
            # the rows in the data are turned into lists for convenience
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

class TableData:
    '''An object with lists of row and column data from a table'''
    ######################## TableData Object Initiation ########################

    # if you can't tell by its size, this class isn't super necessary, I just find object-oriented code to be more readable
    # than using some other iterable
    def __init__(self, columns=[], rows=[]):
        '''initializes a TableData object'''
        ######################## Data Integrity ########################

        if type(columns) not in [type(()), type([])]:
            columns = []
        if type(rows) not in [type(()), type([])]:
            rows = []
        
        ######################## Row & Column Initiation ########################

        self.columns = list(columns)
        self.rows = list(rows) 

######################## Useful Function Creation ########################

def getTableData(tableName='', columns='*', where='', order=''):
    '''returns a TableData object with the result data from the inputted SQL query'''
    ######################## Data Integrity ########################

    # this just means the columns could be inputted like 
    # 'col1, col2, col3'(as a string) or 
    # ['col1', 'col2', 'col3'] (as a list of strings)
    # it will still be formatted to a string regardless
    try:
        if type(columns) == type([]):
            columns = ', '.join(columns)
    except Exception as e:
        return e

    # these just make sure the where and order by clauses are properly formatted
    try:
        if len(where) > 0 and 'WHERE' not in where.upper(): where = 'WHERE ' + where
        if len(order) > 0 and 'ORDER BY' not in order.upper(): order = 'ORDER BY ' + order
    except Exception as e:
        return e
    
    ######################## SQL Querying & Output ########################

    qryStr = f'Select {columns} from {tableName} {where} {order}'
    qryResultData = DB.query(qryStr)
    columns, rows = qryResultData.columns, qryResultData.rows
    return TableData(columns, rows)

def buildTree(columnNames=[], rows=[], parent= None, scrollBar=None, columnWidth=130, customHeight=6, customPadding=5):
    '''returns a Tkinter Treeview Object based on the inputs'''
    ######################## Data Integrity ########################

    # makes sure there is a place to put the tree. if not, don't make the tree
    if parent == None:
        print('Tree object needs a parent object')
        return None
    
    # makes sure a scrollbar is being used if inputted
    sbcommand = None
    if scrollBar is not None:
        sbcommand = scrollBar.set

    # making sure the column names is formatted into a list of strings
    if type(columnNames) == type(''):
        columnNames = columnNames.split(', ')
    elif type(columnNames) not in [type(()), type([])]:
        columnNames = ['']
    else:
        columnNames = list(columnNames)
    
    # making sure these values are integers
    if type(customHeight) not in [type(0), type('0'), type(0.0)]:
        customHeight = 6
    else:
        customHeight = int(eval(str(customHeight)))
    
    if type(customPadding) not in [type(0), type('0'), type(0.0)]:
        customPadding = 5
    else:
        customPadding = int(eval(str(customPadding)))

    ######################## Tree Creation ########################
    
    try:
        # creates the tree with all of the inputted values called T
        T = ttk.Treeview(master=parent, columns=columnNames, show='headings', height=customHeight, padding=customPadding, yscrollcommand=sbcommand)
        # inserts all of the inputted column with their names to T
        for i in range(len(columnNames)):
            T.column('# '+str(i+1), anchor=tk.CENTER, width=columnWidth)
            T.heading('# '+str(i+1), text=columnNames[i])
        # inserts all of the inputted rows to T
        for row in [list(r) for r in rows]:
            T.insert('', tk.END, text=row, values=row)
        return T
    except Exception as e:
        print(e)
        return None 
    
######################## Database Connection Creation ########################

DB = DatabaseManager(
    server='68.44.168.125', # the server ip goes here
    db='KeeganDB', # database name goes here
    uid='Keegan', # username goes here
    pwd='svu090') # password goes here

######################## Program Start ########################

def main():
    ######################## GUI Window Creation ########################

    window = tk.Tk()
    window.title('Update Hours')

    ######################## Employee GUI Objects Creation ########################

    # gets data from the employee name view to populate the tree
    employeeTableData = getTableData('EmployeeName_View')
    # creates a frame to put all the employee-related GUI objects into one area
    employeeInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    employeeInfoFrm.pack(anchor='w') # adds the frame onto the window
    employeeLabel = tk.Label(master=employeeInfoFrm, text='Employee:')
    employeeLabel.grid(column=0,row=0, sticky='w') # adds the label to the top left of the frame
    employeeSb = tk.Scrollbar(master=employeeInfoFrm, orient='vertical')
    employeeSb.grid(column=1,row=1,sticky='ns')
    # creates a visual table with the data from the Employee Table
    employeeTree = buildTree(columnNames=employeeTableData.columns, rows=employeeTableData.rows, parent=employeeInfoFrm, scrollBar=employeeSb)
    employeeSb.config(command=employeeTree.yview)
    employeeTree.grid(column=0,row=1)

    ######################## Employee Table Event Creation ########################

    def employeeTreeHandler(e = None):
        try:
            # gets the employeeNum from the selected employee if one is selected
            employeeNum = employeeTree.item(employeeTree.focus())['values'][0]
            # gets the project data for the selected employee
            projectTableData = getTableData('ProjectHrsWorkedEmpNum_View', where=f'EmployeeNum = {employeeNum}', columns='ProjectID, ProjectName, HoursWorked')
            # clears the current data from the visual project table and adds the data for the selected employee
            projectTree.delete(*projectTree.get_children())
            for row in projectTableData.rows:
                projectTree.insert('', tk.END, text=row[0], values=row)
        except Exception as e:
            print(e)
    # adds the clicking even for when the visual employee table is clicked on
    employeeTree.bind('<ButtonRelease-1>', employeeTreeHandler)

    ######################## Project GUI Objects Creation ########################

    # gets data from the ProjectHrsWorkedEmpNum_View to populate the tree
    projectTableData = getTableData('ProjectHrsWorkedEmpNum_View', columns='ProjectID, ProjectName, HoursWorked')
    # creates a frame to put all the project-related GUI objects into one area
    projectInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    projectInfoFrm.pack(anchor='w')
    projectLabel = tk.Label(master=projectInfoFrm, text='Project:')
    projectLabel.grid(column=0,row=0, sticky='w')
    projectSb = tk.Scrollbar(master=projectInfoFrm, orient='vertical')
    projectSb.grid(column=1,row=1,sticky='ns')
    # creates a visual table with the data from the Project Table
    projectTree = buildTree(projectTableData.columns, [], projectInfoFrm, projectSb)
    projectSb.config(command=projectTree.yview)
    projectTree.grid(column=0,row=1)

    ######################## Project Table Event Creation ########################

    def projectTreeHandler(e=None):
        try:
            # clears the text from the HoursWorked textbox and inserts the HoursWorked data for the selected project & employee
            hoursWorkedTxt.delete('1.0', tk.END)
            hoursWorkedTxt.insert(tk.END, projectTree.item(projectTree.focus())['values'][2])
        except Exception as e:
            print(e)
    projectTree.bind('<ButtonRelease-1>', projectTreeHandler)

    ######################## HoursWorked Update GUI Objects Creation ########################

    # creates a place for all the HoursWork Update-related GUI objects
    hoursWorkedInfoFrm = tk.Frame(master=window, relief=tk.GROOVE, padx=50, pady=10)
    hoursWorkedInfoFrm.pack(anchor='w')
    hoursWorkedLbl = tk.Label(master=hoursWorkedInfoFrm,text='Hours Worked: ')
    hoursWorkedLbl.grid(column=0,row=0)
    # creates a text box that is used to show and update the HoursWorked data for the selected project & employee
    hoursWorkedTxt = tk.Text(master=hoursWorkedInfoFrm,width=15, height=1)
    hoursWorkedTxt.grid(column=1,row=0, sticky='w')

    ######################## HoursWorked Update Button Event Creation ########################

    def updateDatabase(e=None):
        try:
            projectID = projectTree.item(projectTree.focus())['values'][0]
            employeeNum = employeeTree.item(employeeTree.focus())['values'][0]
            newHoursWorked = hoursWorkedTxt.get('1.0', 'end')
            newHoursWorked = float(newHoursWorked)
            cmdStr = f'execute UpdateAssignment {projectID}, {employeeNum}, {newHoursWorked}'
            print(cmdStr)
            DB.command(cmdStr)
            employeeTreeHandler()
        except Exception as e:
            print(e)

    ######################## HoursWorked Update Button Creation ########################

    updateBtn = tk.Button(master=hoursWorkedInfoFrm, text='Update', command=updateDatabase)
    updateBtn.grid(column=2,row=0)

    ######################## That's all, folks ########################

    window.mainloop()

main()