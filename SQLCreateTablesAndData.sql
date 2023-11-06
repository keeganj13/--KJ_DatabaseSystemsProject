DROP TABLE IF EXISTS Assignment;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Employee;

CREATE TABLE Project(
	ProjectID	Int		NOT NULL,
	Name		varchar(25)	NOT NULL,
	Department	varchar(100)	NULL,
	MaxHours	Numeric(6,2)	Default 100,
	CONSTRAINT ProjectPK PRIMARY KEY(ProjectID));

CREATE TABLE Employee(
	EmployeeNum	Int		NOT NULL,
	FirstName	varchar(10)	NOT NULL,
	LastName	varchar(15)	NOT NULL,
	Phone		char(8),
	Department	varChar(100),
	CONSTRAINT EmployeePK PRIMARY KEY(EmployeeNum));

CREATE TABLE Assignment(
	ProjectID	Int		NOT NULL,
	EmployeeNum	Int		NOT NULL,
	HoursWorked	Numeric(5,2),
	CONSTRAINT AssignmentPK PRIMARY KEY(ProjectID, EmployeeNum),
	CONSTRAINT EmployeeFK FOREIGN KEY(EmployeeNum)
		REFERENCES Employee(EmployeeNum)
			ON UPDATE CASCADE
			ON DELETE NO ACTION,
	CONSTRAINT ProjectFK FOREIGN KEY(ProjectID)
		REFERENCES Project(ProjectID)
			ON UPDATE CASCADE
			ON DELETE CASCADE);

INSERT INTO Project VALUES (1000, 'Q3 Portfolio Analysis', 'Finance', 75);
INSERT INTO Project VALUES (1200, 'Q3 Tax Prep', 'Accounting', 145);
INSERT INTO Project VALUES (1400, 'Q4 Product Plan', 'Marketing', 138);
INSERT INTO Project VALUES (1500, 'Q4 Portfolio Analysis', 'Finance', 110);

INSERT INTO Employee VALUES (100, 'Mary', 'Jacobs', '285-8879', 'Accounting');
INSERT INTO Employee VALUES (200, 'Kenji', 'Numoto', '287-0098', 'Marketing');
INSERT INTO Employee VALUES (300, 'Heather', 'Jones', '287-9981', 'Finance');
INSERT INTO Employee VALUES (400, 'Rosalie', 'Jackson', '285-1273', 'Accounting');
INSERT INTO Employee VALUES (500, 'James', 'Nestor', NULL, 'Info Systems');
INSERT INTO Employee VALUES (600, 'Richard', 'Wu', '287-0123', 'Info Systems');
INSERT INTO Employee VALUES (700, 'Kim', 'Sung', '287-3222', 'Marketing');
INSERT INTO Employee VALUES (800, 'Samuel', 'Hill', '285-8778', 'Info Systems');


INSERT INTO Assignment VALUES (1000, 100, 17.50);
INSERT INTO Assignment VALUES (1000, 300, 12.50);
INSERT INTO Assignment VALUES (1000, 400, 8.00);
INSERT INTO Assignment VALUES (1000, 500, 20.25);
INSERT INTO Assignment VALUES (1200, 100, 45.75);
INSERT INTO Assignment VALUES (1200, 600, 40.50);
INSERT INTO Assignment VALUES (1400, 200, 75.00);
INSERT INTO Assignment VALUES (1400, 700, 20.25);
INSERT INTO Assignment VALUES (1400, 500, 25.25);

