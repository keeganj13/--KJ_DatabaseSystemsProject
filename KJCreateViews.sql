DROP VIEW IF EXISTS TrainerQualification_View;
DROP VIEW IF EXISTS TrainerName_View;

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
