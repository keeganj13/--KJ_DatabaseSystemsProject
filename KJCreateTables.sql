DROP TABLE IF EXISTS ScheduledActivity;
DROP TABLE IF EXISTS Qualification;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Locker;
DROP TABLE IF EXISTS ApprovedActivity;
DROP TABLE IF EXISTS GeneralActivity;
DROP TABLE IF EXISTS ActivityLevel;

CREATE TABLE ActivityLevel(
    LevelType       varchar(15) NOT NULL,
    CONSTRAINT ActivityLevelPK PRIMARY KEY(LevelType)
);

CREATE TABLE GeneralActivity(
    ActivityName    varchar(25) NOT NULL,
    CONSTRAINT GeneralActivityPK PRIMARY KEY(ActivityName)
);

CREATE TABLE ApprovedActivity(
    LevelType       varchar(15) NOT NULL,
    ActivityName    varchar(25) NOT NULL,
    CONSTRAINT ApprovedActivityPK PRIMARY KEY(LevelType, ActivityName),
    CONSTRAINT ApprovedActivityLevelFK FOREIGN KEY(LevelType)
        REFERENCES ActivityLevel(LevelType)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT ApprovedActivityNameFK FOREIGN KEY(ActivityName)
        REFERENCES GeneralActivity(ActivityName)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE Locker(
    LockerNum       Int         NOT NULL,
    CONSTRAINT LockerPK PRIMARY KEY(LockerNum)
);

CREATE TABLE Trainer(
    TrainerID       Int         NOT NULL,
    LockerNum       Int         NOT NULL,
    LastName        varchar(15) NOT NULL,
    FirstName       varchar(15) NOT NULL,
    Email           varchar(50) NULL,
    PhoneNum        varchar(14) NULL,
    CONSTRAINT TrainerPK PRIMARY KEY(TrainerID),
    CONSTRAINT TrainerLockerFK FOREIGN KEY(LockerNum)
        REFERENCES Locker(LockerNum)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE Qualification(
    TrainerID       Int         NOT NULL,
    LevelType       varchar(15) NOT NULL,
    ActivityName    varchar(25) NOT NULL,
    ApprovalDate    varchar(10) NULL,
    CONSTRAINT QualificationPK PRIMARY KEY(TrainerID, LevelType, ActivityName),
    CONSTRAINT QualificationTrainerFK FOREIGN KEY(TrainerID)
        REFERENCES Trainer(TrainerID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT QualificationLevelNameFK FOREIGN KEY(LevelType, ActivityName)
        REFERENCES ApprovedActivity(LevelType, ActivityName)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE ScheduledActivity(
    TrainerID       Int         NOT NULL,
    LevelType       varchar(15) NOT NULL,
    ActivityName    varchar(25) NOT NULL,
    StartDate       varchar(10) NOT NULL,
    StartTime       varchar(10) NULL,
    EndTime         varchar(10) NULL,
    CONSTRAINT ScheduledActivityPK PRIMARY KEY(TrainerID, LevelType, ActivityName),
    CONSTRAINT ScheduledActivityTrainerFK FOREIGN KEY(TrainerID)
        REFERENCES Trainer(TrainerID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT ScheduledActivityLevelNameFK FOREIGN KEY(LevelType, ActivityName)
        REFERENCES ApprovedActivity(LevelType, ActivityName)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

-- INSERT INTO Locker VALUES (LockerNum);
INSERT INTO Locker VALUES (01);
INSERT INTO Locker VALUES (02);
INSERT INTO Locker VALUES (03);
INSERT INTO Locker VALUES (04);
INSERT INTO Locker VALUES (05);

-- INSERT INTO Trainer VALUES (TrainerID, LockerNum, LastName, FirstName, Email, PhoneNum);
INSERT INTO Trainer VALUES (101, 01, 'Smith', 'Kendrick', 'ksmizzy@gmail.com', '1-333-242-6784');
INSERT INTO Trainer VALUES (102, 02, 'Kent', 'Clark', 'notsuperman@hotmail.com', '1-555-796-2214');
INSERT INTO Trainer VALUES (103, 03, 'Hobbs', 'Fiona', 'fh1990@gmail.com', '1-888-276-6333');
INSERT INTO Trainer VALUES (104, 04, 'Brown', 'Jarod', 'jbrown49@yahoo.com', '1-456-788-1149');
INSERT INTO Trainer VALUES (105, 05, 'Carrey', 'Cassandra', 'ccarr11@gmail.com', '1-145-555-1689');

-- INSERT INTO GeneralActivity VALUES (ActivityName);
INSERT INTO GeneralActivity VALUES ('Spinning');
INSERT INTO GeneralActivity VALUES ('Yoga');
INSERT INTO GeneralActivity VALUES ('Zumba');
INSERT INTO GeneralActivity VALUES ('Pilates');
INSERT INTO GeneralActivity VALUES ('Crossfit');

-- INSERT INTO ActivityLevel VALUES (LevelType);
INSERT INTO ActivityLevel VALUES ('Beginner');
INSERT INTO ActivityLevel VALUES ('Easy');
INSERT INTO ActivityLevel VALUES ('Intermediate');
INSERT INTO ActivityLevel VALUES ('Intense');
INSERT INTO ActivityLevel VALUES ('Expert');

-- INSERT INTO ApprovedActivity VALUES (LevelType, ActivityName);
INSERT INTO ApprovedActivity VALUES ('Beginner', 'Crossfit');
INSERT INTO ApprovedActivity VALUES ('Beginner', 'Spinning');
INSERT INTO ApprovedActivity VALUES ('Beginner', 'Pilates');
INSERT INTO ApprovedActivity VALUES ('Easy', 'Zumba');
INSERT INTO ApprovedActivity VALUES ('Easy', 'Pilates');
INSERT INTO ApprovedActivity VALUES ('Intermediate', 'Spinning');
INSERT INTO ApprovedActivity VALUES ('Intermediate', 'Yoga');
INSERT INTO ApprovedActivity VALUES ('Intense', 'Crossfit');
INSERT INTO ApprovedActivity VALUES ('Intense', 'Zumba');
INSERT INTO ApprovedActivity VALUES ('Expert', 'Pilates');
INSERT INTO ApprovedActivity VALUES ('Expert', 'Yoga');

-- INSERT INTO Qualification VALUES (TrainerID, LevelType, ActivityName, ApprovalDate);
INSERT INTO Qualification VALUES (101, 'Beginner', 'Spinning', '10-09-2017');
INSERT INTO Qualification VALUES (101, 'Easy', 'Pilates', '02-20-2019');
INSERT INTO Qualification VALUES (101, 'Intense', 'Crossfit', '02-08-2023');
INSERT INTO Qualification VALUES (101, 'Easy', 'Zumba', '04-19-2018');

INSERT INTO Qualification VALUES (102, 'Beginner', 'Spinning', '03-15-2016');
INSERT INTO Qualification VALUES (102, 'Easy', 'Pilates', '01-10-2018');
INSERT INTO Qualification VALUES (102, 'Intermediate', 'Spinning', '08-17-2020');

INSERT INTO Qualification VALUES (103, 'Beginner', 'Crossfit', '10-01-2017');
INSERT INTO Qualification VALUES (103, 'Intermediate', 'Yoga', '07-22-2020');
INSERT INTO Qualification VALUES (103, 'Expert', 'Yoga', '05-14-2023');

INSERT INTO Qualification VALUES (104, 'Beginner', 'Crossfit', '06-08-2015');
INSERT INTO Qualification VALUES (104, 'Intermediate', 'Yoga', '03-14-2021');
INSERT INTO Qualification VALUES (104, 'Intense', 'Zumba', '12-02-2022');

INSERT INTO Qualification VALUES (105, 'Beginner', 'Spinning', '06-04-2016');
INSERT INTO Qualification VALUES (105, 'Easy', 'Zumba', '08-17-2018');
INSERT INTO Qualification VALUES (105, 'Beginner', 'Pilates', '11-04-2020');

-- INSERT INTO ScheduledActivity VALUES (TrainerID, LevelType, ActivityName, StartDate, StartTime, EndTime);
INSERT INTO ScheduledActivity VALUES (101, 'Beginner', 'Spinning', '11-09-2023', '6:00pm', '7:30pm');
INSERT INTO ScheduledActivity VALUES (101, 'Intense', 'Crossfit', '11-08-2023', '2:00pm', '3:00pm');
INSERT INTO ScheduledActivity VALUES (101, 'Easy', 'Zumba', '11-20-2023', '1:00pm', '3:00pm');
INSERT INTO ScheduledActivity VALUES (101, 'Easy', 'Pilates', '11-19-2023', '2:00pm', '3:00pm');

INSERT INTO ScheduledActivity VALUES (102, 'Easy', 'Pilates', '11-10-2023', '1:00pm', '3:00pm');
INSERT INTO ScheduledActivity VALUES (102, 'Beginner', 'Spinning', '11-15-2023', '6:00pm', '7:30pm');
INSERT INTO ScheduledActivity VALUES (102, 'Intermediate', 'Spinning', '11-17-2023', '6:00pm', '7:30pm');

INSERT INTO ScheduledActivity VALUES (103, 'Beginner', 'Crossfit', '11-06-2023', '5:00pm', '6:30pm');
INSERT INTO ScheduledActivity VALUES (103, 'Intermediate', 'Yoga', '11-22-2023', '4:00pm', '5:00pm');
INSERT INTO ScheduledActivity VALUES (103, 'Expert', 'Yoga', '11-14-2023', '1:00pm', '3:00pm');

INSERT INTO ScheduledActivity VALUES (104, 'Beginner', 'Crossfit', '11-08-2023', '5:00pm', '6:30pm');
INSERT INTO ScheduledActivity VALUES (104, 'Intermediate', 'Yoga', '11-14-2023', '1:00pm', '3:00pm');

INSERT INTO ScheduledActivity VALUES (105, 'Beginner', 'Pilates', '11-04-2023', '4:00pm', '5:00pm');
INSERT INTO ScheduledActivity VALUES (105, 'Easy', 'Zumba', '11-17-2023', '5:00pm', '6:30pm');
INSERT INTO ScheduledActivity VALUES (105, 'Beginner', 'Spinning', '11-15-2023', '6:00pm', '7:30pm');
