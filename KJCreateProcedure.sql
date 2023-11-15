DROP PROCEDURE IF EXISTS UpdateApprovalDate;

CREATE PROCEDURE UpdateApprovalDate
    @TID INT,
    @LvlType VARCHAR(15),
    @ActName VARCHAR(25),
    @ApprvlDate VARCHAR(10) 
AS 
    UPDATE  Qualification
    SET     ApprovalDate = @ApprvlDate
    WHERE   TrainerID = @TID AND 
            LevelType = @LvlType AND 
            ActivityName = @ActName;