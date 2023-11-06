DROP VIEW IF EXISTS ProjectHrsWorkedEmpNum_View;

CREATE VIEW ProjectHrsWorkedEmpNum_View AS
SELECT
	A.ProjectID,
	A.EmployeeNum,
	A.HoursWorked,
	P.Name AS ProjectName
FROM
	Assignment A
JOIN
	Project P
	ON A.ProjectID = P.ProjectID