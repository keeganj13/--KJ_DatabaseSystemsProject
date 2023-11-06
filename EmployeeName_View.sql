DROP VIEW IF EXISTS EmployeeName_View;

CREATE VIEW EmployeeName_View AS
SELECT
	EmployeeNum,
	LastName,
	FirstName
FROM
	Employee