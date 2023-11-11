DROP VIEW IF EXISTS TrainerQualification_View;
DROP VIEW IF EXISTS TrainerName_View;
DROP VIEW IF EXISTS TrainerActivity_View;
DROP VIEW IF EXISTS ApprovedActivity_View;

CREATE VIEW TrainerQualification_View AS (
    SELECT
        T.TrainerID,
        Q.LevelType,
        Q.ActivityName,
        Q.ApprovalDate
    FROM
        Qualification Q
    JOIN
        Trainer T
    ON
        T.TrainerID = Q.TrainerID
);

CREATE VIEW TrainerName_View AS (
    SELECT
        TrainerID,
        LastName,
        FirstName
    FROM
        Trainer
);

CREATE VIEW TrainerActivity_View AS (
    SELECT
        Q.TrainerID,
        Q.LevelType,
        Q.ActivityName,
        S.StartDate,
        S.StartTime,
        S.EndTime
    FROM
        ScheduledActivity S 
    JOIN
        Qualification Q 
    ON
        S.QualificationID = Q.QualificationID
);

CREATE VIEW ApprovedActivity_View AS (
    SELECT
        LevelType, ActivityName
    FROM
        ApprovedActivity
);