DROP TABLE IF EXISTS ScheduledActivity;
DROP TABLE IF EXISTS Qualification;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Locker;
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
    CONSTRAINT QualificationActivityLevelFK FOREIGN KEY(LevelType)
        REFERENCES ActivityLevel(LevelType)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT QualificationGeneralActivityFK FOREIGN KEY(ActivityName)
        REFERENCES GeneralActivity(ActivityName)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE ScheduledActivity(
    TrainerID       Int         NOT NULL,
    LevelType       varchar(15) NOT NULL,
    ActivityName    varchar(25) NOT NULL,
    StartDate       varchar(10) NULL,
    StartTime       varchar(10) NULL,
    EndTime         varchar(10) NULL,
    CONSTRAINT ScheduledActivityPK PRIMARY KEY(TrainerID, LevelType, ActivityName),
    CONSTRAINT ScheduledActivityTrainerFK FOREIGN KEY(TrainerID)
        REFERENCES Trainer(TrainerID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT ScheduledActivityActivityLevelFK FOREIGN KEY(LevelType)
        REFERENCES ActivityLevel(LevelType)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
    CONSTRAINT ScheduledActivityGeneralActivityFK FOREIGN KEY(ActivityName)
        REFERENCES GeneralActivity(ActivityName)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

/* INSERT INTO Locker VALUES (LockerNum) */
INSERT INTO Locker VALUES (01);
INSERT INTO Locker VALUES (02);
INSERT INTO Locker VALUES (03);
INSERT INTO Locker VALUES (04);
INSERT INTO Locker VALUES (05);
INSERT INTO Locker VALUES (06);
INSERT INTO Locker VALUES (07);
INSERT INTO Locker VALUES (08);
INSERT INTO Locker VALUES (09);
INSERT INTO Locker VALUES (10);
INSERT INTO Locker VALUES (11);
INSERT INTO Locker VALUES (12);
INSERT INTO Locker VALUES (13);
INSERT INTO Locker VALUES (14);
INSERT INTO Locker VALUES (15);
INSERT INTO Locker VALUES (16);
INSERT INTO Locker VALUES (17);
INSERT INTO Locker VALUES (18);
INSERT INTO Locker VALUES (19);
INSERT INTO Locker VALUES (20);

/* INSERT INTO Trainer VALUES (TrainerID, LockerNum, LastName, FirstName, Email, PhoneNum) */
INSERT INTO Trainer VALUES (101, 01, 'Smith', 'Kendrick', 'ksmizzy@gmail.com', '1-333-242-6784');
INSERT INTO Trainer VALUES (102, 02, 'Kent', 'Clark', 'notsuperman@hotmail.com', '1-555-796-2214');
INSERT INTO Trainer VALUES (103, 03, 'Hobbs', 'Fiona', 'fh1990@gmail.com', '1-888-276-6333');
INSERT INTO Trainer VALUES (104, 04, 'Brown', 'Jarod', 'jbrown49@yahoo.com', '1-456-788-1149');
INSERT INTO Trainer VALUES (105, 05, 'Carrey', 'Cassandra', 'ccarr11@gmail.com', '1-145-555-1689');
INSERT INTO Trainer VALUES (106, 06, 'Jacobs', 'Mary', NULL, '1-633-285-8879');
INSERT INTO Trainer VALUES (107, 07, 'Numoto', 'Kenji', NULL, '1-900-287-0098');
INSERT INTO Trainer VALUES (108, 08, 'Jones', 'Heather', NULL, '1-235-287-9981');
INSERT INTO Trainer VALUES (109, 09, 'Jackson', 'Rosalie', NULL, '1-877-285-1273');
INSERT INTO Trainer VALUES (110, 10, 'Nestor', 'James', NULL, NULL);
INSERT INTO Trainer VALUES (111, 11, 'Wu', 'Richard', NULL, '1-555-287-0123');
INSERT INTO Trainer VALUES (112, 12, 'Sung', 'Kim', NULL, '1-677-287-3222');
INSERT INTO Trainer VALUES (113, 13, 'Hill', 'Samuel', NULL, '1-819-285-8778');

/* INSERT INTO GeneralActivity VALUES (ActivityName) */
INSERT INTO GeneralActivity VALUES ('Spinning');
INSERT INTO GeneralActivity VALUES ('Yoga');
INSERT INTO GeneralActivity VALUES ('Zumba');
INSERT INTO GeneralActivity VALUES ('Pilates');
INSERT INTO GeneralActivity VALUES ('Crossfit');

/* INSERT INTO ActivityLevel VALUES (LevelType) */
INSERT INTO ActivityLevel VALUES ('Beginner');
INSERT INTO ActivityLevel VALUES ('Easy');
INSERT INTO ActivityLevel VALUES ('Intermediate');
INSERT INTO ActivityLevel VALUES ('Intense');
INSERT INTO ActivityLevel VALUES ('Expert');

/* INSERT INTO Qualification VALUES (TrainerID, LevelType, ActivityName, ApprovalDate) */
INSERT INTO Qualification VALUES (101, 'Beginner', 'Spinning', '10-09-2017');
INSERT INTO Qualification VALUES (102, 'Beginner', 'Spinning', '03-15-2016');
INSERT INTO Qualification VALUES (103, 'Beginner', 'Zumba', '10-01-2017');
INSERT INTO Qualification VALUES (104, 'Beginner', 'Zumba', '06-08-2015');
INSERT INTO Qualification VALUES (105, 'Beginner', 'Pilates', '06-04-2016');
INSERT INTO Qualification VALUES (101, 'Easy', 'Yoga', '02-20-2019');
INSERT INTO Qualification VALUES (105, 'Easy', 'Zumba', '08-17-2018');
INSERT INTO Qualification VALUES (102, 'Easy', 'Yoga', '01-10-2018');
INSERT INTO Qualification VALUES (101, 'Easy', 'Crossfit', '04-19-2018');
INSERT INTO Qualification VALUES (103, 'Intermediate', 'Pilates', '07-22-2020');
INSERT INTO Qualification VALUES (104, 'Intermediate', 'Yoga', '03-14-2021');
INSERT INTO Qualification VALUES (102, 'Intermediate', 'Spinning', '08-17-2020');
INSERT INTO Qualification VALUES (110, 'Intense', 'Spinning', '12-02-2022');
INSERT INTO Qualification VALUES (101, 'Intense', 'Crossfit', '02-08-2023');
INSERT INTO Qualification VALUES (103, 'Expert', 'Yoga', '05-14-2023');

INSERT INTO Qualification VALUES (108, 'Beginner', 'Crossfit', '05-09-2017');
INSERT INTO Qualification VALUES (107, 'Beginner', 'Spinning', '03-18-2016');
INSERT INTO Qualification VALUES (106, 'Beginner', 'Yoga', '10-21-2017');
INSERT INTO Qualification VALUES (109, 'Beginner', 'Zumba', '06-18-2016');
INSERT INTO Qualification VALUES (110, 'Beginner', 'Pilates', '06-04-2016');
INSERT INTO Qualification VALUES (107, 'Easy', 'Yoga', '02-20-2019');
INSERT INTO Qualification VALUES (110, 'Easy', 'Spinning', '08-17-2018');
INSERT INTO Qualification VALUES (106, 'Easy', 'Yoga', '01-10-2018');
INSERT INTO Qualification VALUES (109, 'Easy', 'Pilates', '04-19-2018');
INSERT INTO Qualification VALUES (110, 'Intermediate', 'Spinning', '07-22-2020');
INSERT INTO Qualification VALUES (111, 'Intermediate', 'Yoga', '03-14-2021');
INSERT INTO Qualification VALUES (110, 'Intermediate', 'Crossfit', '08-17-2020');
INSERT INTO Qualification VALUES (106, 'Intense', 'Yoga', '12-02-2022');
INSERT INTO Qualification VALUES (107, 'Intense', 'Crossfit', '02-08-2023');
INSERT INTO Qualification VALUES (108, 'Expert', 'Yoga', '05-14-2023');


INSERT INTO Qualification VALUES (111, 'Beginner', 'Spinning', '10-09-2017');
INSERT INTO Qualification VALUES (112, 'Beginner', 'Spinning', '03-15-2016');
INSERT INTO Qualification VALUES (113, 'Easy', 'Yoga', '02-20-2019');
INSERT INTO Qualification VALUES (113, 'Easy', 'Zumba', '08-17-2018');
INSERT INTO Qualification VALUES (112, 'Intermediate', 'Pilates', '07-22-2020');
INSERT INTO Qualification VALUES (110, 'Intermediate', 'Yoga', '03-14-2021');
INSERT INTO Qualification VALUES (113, 'Intense', 'Spinning', '12-02-2022');
INSERT INTO Qualification VALUES (111, 'Intense', 'Crossfit', '02-08-2023');
INSERT INTO Qualification VALUES (112, 'Expert', 'Yoga', '05-14-2023');

/* INSERT INTO ScheduledActivity VALUES (TrainerID, LevelType, ActivityName, StartDate, StartTime, EndTime) */
INSERT INTO ScheduledActivity VALUES (101, 'Beginner', 'Spinning', '11-09-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (102, 'Beginner', 'Spinning', '11-15-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (103, 'Beginner', 'Zumba', '11-06-2023', '17:00', '18:30');
INSERT INTO ScheduledActivity VALUES (104, 'Beginner', 'Zumba', '11-08-2023', '17:00', '18:30');
INSERT INTO ScheduledActivity VALUES (105, 'Beginner', 'Pilates', '11-04-2023', '16:00', '17:00');
INSERT INTO ScheduledActivity VALUES (101, 'Easy', 'Yoga', '11-20-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (105, 'Easy', 'Zumba', '11-17-2023', '17:00', '18:30');
INSERT INTO ScheduledActivity VALUES (102, 'Easy', 'Yoga', '11-10-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (101, 'Easy', 'Crossfit', '11-19-2023', '14:00', '15:00');
INSERT INTO ScheduledActivity VALUES (103, 'Intermediate', 'Pilates', '11-22-2023', '16:00', '17:00');
INSERT INTO ScheduledActivity VALUES (104, 'Intermediate', 'Yoga', '11-14-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (102, 'Intermediate', 'Spinning', '11-17-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (110, 'Intense', 'Spinning', '11-15-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (101, 'Intense', 'Crossfit', '11-08-2023', '14:00', '15:00');
INSERT INTO ScheduledActivity VALUES (103, 'Expert', 'Yoga', '11-14-2023', '13:00', '15:00');

INSERT INTO ScheduledActivity VALUES (108, 'Beginner', 'Crossfit', '11-09-2023', '14:00', '15:00');
INSERT INTO ScheduledActivity VALUES (107, 'Beginner', 'Spinning', '11-18-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (106, 'Beginner', 'Yoga', '11-21-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (109, 'Beginner', 'Zumba', '11-18-2023', '17:00', '18:30');
INSERT INTO ScheduledActivity VALUES (110, 'Beginner', 'Pilates', '11-14-2023', '16:00', '17:00');
INSERT INTO ScheduledActivity VALUES (107, 'Easy', 'Yoga', '11-20-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (110, 'Easy', 'Spinning', '11-17-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (106, 'Easy', 'Yoga', '11-10-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (109, 'Easy', 'Pilates', '11-19-2023', '16:00', '17:00');
INSERT INTO ScheduledActivity VALUES (110, 'Intermediate', 'Spinning', '11-22-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (111, 'Intermediate', 'Yoga', '11-14-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (110, 'Intermediate', 'Crossfit', '11-17-2023', '14:00', '15:00');
INSERT INTO ScheduledActivity VALUES (106, 'Intense', 'Yoga', '11-12-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (107, 'Intense', 'Crossfit', '11-08-2023', '14:00', '15:00');
INSERT INTO ScheduledActivity VALUES (108, 'Expert', 'Yoga', '11-14-2023', '13:00', '15:00');

INSERT INTO ScheduledActivity VALUES (111, 'Beginner', 'Spinning', '11-09-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (112, 'Beginner', 'Spinning', '11-15-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (113, 'Easy', 'Yoga', '11-20-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (113, 'Easy', 'Zumba', '11-17-2023', '17:00', '18:30');
INSERT INTO ScheduledActivity VALUES (112, 'Intermediate', 'Pilates', '11-22-2023', '16:00', '17:00');
INSERT INTO ScheduledActivity VALUES (110, 'Intermediate', 'Yoga', '11-14-2023', '13:00', '15:00');
INSERT INTO ScheduledActivity VALUES (113, 'Intense', 'Spinning', '11-12-2023', '18:00', '19:30');
INSERT INTO ScheduledActivity VALUES (111, 'Intense', 'Crossfit', '11-08-2023', '14:00', '15:00');
INSERT INTO ScheduledActivity VALUES (112, 'Expert', 'Yoga', '11-14-2023', '13:00', '15:00');