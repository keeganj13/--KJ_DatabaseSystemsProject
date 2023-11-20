DROP TABLE IF EXISTS ScheduledActivity;
DROP TABLE IF EXISTS Qualification;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Locker;
DROP TABLE IF EXISTS ApprovedActivity;
DROP TABLE IF EXISTS GeneralActivity;
DROP TABLE IF EXISTS ActivityLevel;

CREATE TABLE ActivityLevel (
    LevelID         INT         NOT NULL,
    LevelType       VARCHAR(15) NOT NULL,
    LevelDescription VARCHAR(50) NULL,
    CONSTRAINT ActivityLevelPK PRIMARY KEY(LevelID),
    CONSTRAINT UniqueLevel UNIQUE(LevelType)
);

CREATE TABLE GeneralActivity (
    NameID          INT         NOT NULL,
    ActivityName    VARCHAR(25) NOT NULL,
    ActivityDescription VARCHAR(50) NULL,
    CONSTRAINT GeneralActivityPK PRIMARY KEY(NameID),
    CONSTRAINT UniqueName UNIQUE(ActivityName)
);

CREATE TABLE ApprovedActivity (
    LevelType       VARCHAR(15) NOT NULL,
    ActivityName    VARCHAR(25) NOT NULL,
    CONSTRAINT ApprovedActivityPK PRIMARY KEY(LevelType, ActivityName),
    CONSTRAINT ApprovedActivityLevelFK FOREIGN KEY(LevelType)
        REFERENCES ActivityLevel(LevelType)
            ON UPDATE CASCADE
            ON DELETE NO ACTION,
    CONSTRAINT ApprovedActivityNameFK FOREIGN KEY(ActivityName)
        REFERENCES GeneralActivity(ActivityName)
            ON UPDATE CASCADE
            ON DELETE NO ACTION
);

CREATE TABLE Locker (
    LockerNum       INT         NOT NULL,
    CONSTRAINT LockerNumCheck CHECK(LockerNum >= 0 AND LockerNum <= 50),
    CONSTRAINT LockerPK PRIMARY KEY(LockerNum)
);

CREATE TABLE Trainer (
    TrainerID       INT         NOT NULL,
    LockerNum       INT         NOT NULL,
    LastName        VARCHAR(15) NOT NULL,
    FirstName       VARCHAR(15) NOT NULL,
    Email           VARCHAR(50) NOT NULL,
    PhoneNum        VARCHAR(14) NOT NULL,
    CONSTRAINT TrainerIDCheck CHECK(TrainerID > 0),
    CONSTRAINT UniqueEmail UNIQUE(Email),
    CONSTRAINT UniquePhoneNum UNIQUE(PhoneNum),
    CONSTRAINT TrainerPK PRIMARY KEY(TrainerID),
    CONSTRAINT TrainerLockerFK FOREIGN KEY(LockerNum)
        REFERENCES Locker(LockerNum)
            ON UPDATE CASCADE
            ON DELETE NO ACTION
);

CREATE TABLE Qualification (
    QualificationID INT         NOT NULL,
    TrainerID       INT         NOT NULL,
    LevelType       VARCHAR(15) NOT NULL,
    ActivityName    VARCHAR(25) NOT NULL,
    ApprovalDate    DATE        NULL,
    CONSTRAINT ApprovalDateCheck CHECK(ApprovalDate <= GETDATE()),
    CONSTRAINT UniqueQualification UNIQUE(TrainerID, LevelType, ActivityName),
    CONSTRAINT QualificationPK PRIMARY KEY(QualificationID),
    CONSTRAINT QualificationTrainerFK FOREIGN KEY(TrainerID)
        REFERENCES Trainer(TrainerID)
            ON UPDATE CASCADE
            ON DELETE NO ACTION,
    CONSTRAINT QualificationActivityFK FOREIGN KEY(LevelType, ActivityName)
        REFERENCES ApprovedActivity(LevelType, ActivityName)
            ON UPDATE CASCADE
            ON DELETE NO ACTION
);

CREATE TABLE ScheduledActivity (
    QualificationID INT         NOT NULL,
    StartDate       DATE        NOT NULL,
    StartTime       VARCHAR(10) NOT NULL,
    EndTime         VARCHAR(10) NULL,
    CONSTRAINT StartDateCheck CHECK(StartDate >= getdate()),
    CONSTRAINT ScheduledActivityPK PRIMARY KEY(QualificationID, StartDate, StartTime),
    CONSTRAINT ScheduledActivityFK FOREIGN KEY(QualificationID)
        REFERENCES Qualification(QualificationID)
            ON UPDATE CASCADE
            ON DELETE NO ACTION
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

-- INSERT INTO GeneralActivity VALUES (NameID, ActivityName, ActivityDescription);
INSERT INTO GeneralActivity VALUES (1, 'Spinning', '');
INSERT INTO GeneralActivity VALUES (2, 'Yoga', '');
INSERT INTO GeneralActivity VALUES (3, 'Zumba', '');
INSERT INTO GeneralActivity VALUES (4, 'Pilates', '');
INSERT INTO GeneralActivity VALUES (5, 'Crossfit', '');

-- INSERT INTO ActivityLevel VALUES (LevelID, LevelType, LevelDescription);
INSERT INTO ActivityLevel VALUES (1, 'Beginner', '');
INSERT INTO ActivityLevel VALUES (2, 'Easy', '');
INSERT INTO ActivityLevel VALUES (3, 'Intermediate', '');
INSERT INTO ActivityLevel VALUES (4, 'Intense', '');
INSERT INTO ActivityLevel VALUES (5, 'Expert', '');

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

-- INSERT INTO Qualification VALUES (QualificationID, TrainerID, LevelType, ActivityName, ApprovalDate);
INSERT INTO Qualification VALUES (01, 101, 'Beginner', 'Spinning', '2017-10-09');
INSERT INTO Qualification VALUES (02, 101, 'Easy', 'Pilates', '2019-02-20');
INSERT INTO Qualification VALUES (03, 101, 'Intense', 'Crossfit', '2023-02-08');
INSERT INTO Qualification VALUES (04, 101, 'Easy', 'Zumba', '2018-04-19');

INSERT INTO Qualification VALUES (05, 102, 'Beginner', 'Spinning', '2016-03-15');
INSERT INTO Qualification VALUES (06, 102, 'Easy', 'Pilates', '2018-01-10');
INSERT INTO Qualification VALUES (07, 102, 'Intermediate', 'Spinning', '2020-08-17');

INSERT INTO Qualification VALUES (08, 103, 'Beginner', 'Crossfit', '2017-10-01');
INSERT INTO Qualification VALUES (09, 103, 'Intermediate', 'Yoga', '2020-07-22');
INSERT INTO Qualification VALUES (10, 103, 'Expert', 'Yoga', '2023-05-14');

INSERT INTO Qualification VALUES (11, 104, 'Beginner', 'Crossfit', '2015-06-08');
INSERT INTO Qualification VALUES (12, 104, 'Intermediate', 'Yoga', '2021-03-14');
INSERT INTO Qualification VALUES (13, 104, 'Intense', 'Zumba', '2022-12-02');

INSERT INTO Qualification VALUES (14, 105, 'Beginner', 'Spinning', '2016-06-04');
INSERT INTO Qualification VALUES (15, 105, 'Easy', 'Zumba', '2018-08-17');
INSERT INTO Qualification VALUES (16, 105, 'Beginner', 'Pilates', '2020-11-04');

-- INSERT INTO ScheduledActivity VALUES (QualificationID, StartDate, StartTime, EndTime);
INSERT INTO ScheduledActivity VALUES (01, '2023-12-09', '6:00pm', '7:30pm');
INSERT INTO ScheduledActivity VALUES (03, '2023-12-08', '2:00pm', '3:00pm');
INSERT INTO ScheduledActivity VALUES (04, '2023-12-20', '1:00pm', '3:00pm');
INSERT INTO ScheduledActivity VALUES (02, '2023-12-19', '2:00pm', '3:00pm');

INSERT INTO ScheduledActivity VALUES (06, '2023-12-10', '1:00pm', '3:00pm');
INSERT INTO ScheduledActivity VALUES (05, '2023-12-15', '6:00pm', '7:30pm');
INSERT INTO ScheduledActivity VALUES (07, '2023-12-17', '6:00pm', '7:30pm');

INSERT INTO ScheduledActivity VALUES (08, '2023-12-06', '5:00pm', '6:30pm');
INSERT INTO ScheduledActivity VALUES (09, '2023-12-22', '4:00pm', '5:00pm');
INSERT INTO ScheduledActivity VALUES (10, '2023-12-14', '1:00pm', '3:00pm');

INSERT INTO ScheduledActivity VALUES (11, '2023-12-08', '5:00pm', '6:30pm');
INSERT INTO ScheduledActivity VALUES (12, '2023-12-14', '1:00pm', '3:00pm');

INSERT INTO ScheduledActivity VALUES (16, '2023-12-04', '4:00pm', '5:00pm');
INSERT INTO ScheduledActivity VALUES (15, '2023-12-17', '5:00pm', '6:30pm');
INSERT INTO ScheduledActivity VALUES (14, '2023-12-15', '6:00pm', '7:30pm');
