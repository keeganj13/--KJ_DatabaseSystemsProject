DROP VIEW IF EXISTS TrainerQualification_View;
DROP VIEW IF EXISTS TrainerName_View;
DROP VIEW IF EXISTS TrainerActivity_View;

CREATE VIEW TrainerQualification_View AS
SELECT
    T.TrainerID,
    T.LastName,
    T.FirstName,
    Q.LevelType,
    Q.ActivityName,
    Q.ApprovalDate
FROM
    Qualification Q
JOIN
    Trainer T
ON
    T.TrainerID = Q.TrainerID;

CREATE VIEW TrainerName_View AS
SELECT
    TrainerID,
    LastName,
    FirstName
FROM
    Trainer;

CREATE VIEW TrainerActivity_View AS
SELECT
    T.TrainerID,
    T.LastName,
    T.FirstName,
    S.LevelType,
    S.ActivityName,
    S.StartDate,
    S.StartTime,
    S.EndTime
FROM
    ScheduledActivity S 
JOIN
    Trainer T 
ON
    S.TrainerID = T.TrainerID;