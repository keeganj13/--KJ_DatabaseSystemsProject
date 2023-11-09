CREATE TABLE Publisher
	(
	PubName		VARCHAR(25)	NOT NULL,
	City		VARCHAR(25),
	Country 	VARCHAR(25),
	Telephone 	VARCHAR(15),
	YrFounded	NUMERIC(4),
	CONSTRAINT 	PublisherPK	PRIMARY KEY (PubName)
	);

CREATE TABLE Author
	(
	AuthorNum	INT NOT NULL,
	AuthorName	VARCHAR(25),
	YearBorn	NUMERIC(4),
	YearDied	NUMERIC(4),
	CONSTRAINT 	AuthorPK 	PRIMARY KEY (AuthorNum),
	CONSTRAINT 	DeceaseDateCheck  CHECK (YearDied > YearBorn)
	);

CREATE TABLE Customer
	(
	CustNum		INT		NOT NULL,
	CustName 	VARCHAR(25),
	Street 		VARCHAR(30),
	City 		VARCHAR(20),
	State		VARCHAR(20),
	Country		VARCHAR(25),
	CONSTRAINT 	CustomerPK	PRIMARY KEY (CustNum)
	);

CREATE TABLE Book
	(
	BookNum		INT		NOT NULL,
	BookName	VARCHAR(30),
	PubYear		NUMERIC(4),
	Pages		INT,
	PubName		VARCHAR(25)	NOT NULL,
	CONSTRAINT 	BookPK	PRIMARY KEY (BookNum),
	CONSTRAINT	PublisherFK	FOREIGN KEY (PubName)
				REFERENCES Publisher (PubName)
	);

CREATE TABLE Writing
	(
	BookNum		INT		NOT NULL,
	AuthorNum	INT		NOT NULL,
	CONSTRAINT 	WritingPK 	PRIMARY KEY (BookNum, AuthorNum),
	CONSTRAINT	BookFK		FOREIGN KEY (BookNum) REFERENCES Book (BookNum),
	CONSTRAINT	AuthorFK	FOREIGN KEY (AuthorNum) REFERENCES Author (AuthorNum)
	);

CREATE TABLE Sale
	(
	BookNum		INT		NOT NULL,
	CustNum		INT		NOT NULL,
	SaleDate	Date		NOT NULL,
	Price		NUMERIC(5,2)	NOT NULL,
	Quantity	INT		NOT NULL,
	CONSTRAINT 	SalePK 		PRIMARY KEY (BookNum, CustNum),
	CONSTRAINT	BookSaleFK	FOREIGN KEY (BookNum)
				REFERENCES Book (BookNum),
	CONSTRAINT	CustSaleFK	FOREIGN KEY (CustNum)
				REFERENCES Customer (CustNum)
	);

INSERT INTO Publisher VALUES ('African Publishing', 'Nairobi', 'Kenya', '254 345 767', 1964)
INSERT INTO Publisher VALUES ('Asian Publishers', 'Singapore', 'Singapore', '65 554 328', 1937)
INSERT INTO Publisher VALUES ('Belgian Publishing', 'Brussels', 'Belgium', '32 447 372', 2000)
INSERT INTO Publisher VALUES ('Elmers Publishing', 'New York', 'New York', '1 212 555', 1946)
INSERT INTO Publisher VALUES ('French Publishing', 'Paris', 'France', '33 877 123', 1887)
INSERT INTO Publisher VALUES ('Kenya Publishers', 'Nairobi', 'Kenya', '254 483 876', 1985)
INSERT INTO Publisher VALUES ('London Publishing Ltd', 'London', 'United Kingdom', '44 635 432', 1935)
INSERT INTO Publisher VALUES ('Mardi Gras Publishers', 'Sao Paulo', 'Brazil', '55 384 222', 1978)
INSERT INTO Publisher VALUES ('Norway Publishers', 'Oslo', 'Norway', '47 848 283', 2000)
INSERT INTO Publisher VALUES ('Pacific Publishers', 'Auckland', 'New Zealand', '64 754 666', 1927)
INSERT INTO Publisher VALUES ('Parisian Ltd', 'Paris', 'France', '33 848 101', 1986)
INSERT INTO Publisher VALUES ('Rio Publishing', 'Rio de Janeiro', 'Brazil', '55 473 223', 1954)
INSERT INTO Publisher VALUES ('Viking Publishers', 'Oslo', 'Norway', '47 483 382', 1919)

INSERT INTO Author VALUES (1203, 'Reyes', 1918, 2004)
INSERT INTO Author VALUES (1484, 'Carter', 1939, 2006)
INSERT INTO Author VALUES (2938, 'Baker', 1956, NULL)
INSERT INTO Author VALUES (3101, 'Taylor', 1947, NULL)
INSERT INTO Author VALUES (3800, 'Peres', 1916, 1995)
INSERT INTO Author VALUES (3818, 'Lucas', 1917, 1991)
INSERT INTO Author VALUES (4286, 'Adams', 1918, 2002)
INSERT INTO Author VALUES (4391, 'Wang', 1916, 1999)
INSERT INTO Author VALUES (6327, 'Chen', 1915, 2001)
INSERT INTO Author VALUES (8294, 'Zhang', 1934, NULL)
INSERT INTO Author VALUES (9476, 'Story', 1910, 1987)

INSERT INTO Customer VALUES (4838, 'Norton', '384 Wilcox St', 'London', NULL, 'United Kingdom')
INSERT INTO Customer VALUES (16838, 'Perez', '34 E 96 St', 'New York', 'NY', 'USA')
INSERT INTO Customer VALUES (18384, 'Young', '8533 Central Ave', 'London', NULL, 'United Kingdom')
INSERT INTO Customer VALUES (28941, 'Gomez', '555 4th Ave', 'Sao Paulo', NULL, 'Brazil')
INSERT INTO Customer VALUES (32728, 'Stein', '824 Norway St', 'Oslo', NULL, 'Norway')
INSERT INTO Customer VALUES (32834, 'Simpson', '19 Elm St', 'Memphis', 'TN', 'USA')
INSERT INTO Customer VALUES (48292, 'Martin', '374 Main St', 'Paris', NULL, 'France')
INSERT INTO Customer VALUES (53719, 'Williams', '66 Old Ave', 'London', NULL, 'United Kingdom')
INSERT INTO Customer VALUES (58100, 'Parker', '23 Fifth Ave', 'New York', 'NY', 'USA')
INSERT INTO Customer VALUES (73402, 'Gaulle', '887 Montmarte', 'Paris', NULL, 'France')
INSERT INTO Customer VALUES (81477, 'Zhen', '123 Kirby Rd', 'Singapore', NULL, 'Singapore')
INSERT INTO Customer VALUES (82874, 'Lucas', '38 Ave Winchester', 'Brussels', NULL, 'Belgium')
INSERT INTO Customer VALUES (84231, 'Klein', '33 Sweden St', 'Oslo', NULL, 'Norway')

INSERT INTO Book VALUES (24728, 'Mardi Gras Fun', 1967, 492,  'Mardi Gras Publishers')
INSERT INTO Book VALUES (31732, 'The Belgian Coast', 1937, 258,  'Belgian Publishing')
INSERT INTO Book VALUES (154299, 'Happy Cooking', 1948, 472,  'London Publishing Ltd')
INSERT INTO Book VALUES (184284, 'The Amazon River', 1964, 328,  'Rio Publishing')
INSERT INTO Book VALUES (195587, 'Africa Today', 2000, 429,  'African Publishing')
INSERT INTO Book VALUES (245928, 'Waterfalls', 1923, 285,  'Parisian Ltd')
INSERT INTO Book VALUES (295738, 'Scandinavian History', 2001, 531,  'Viking Publishers')
INSERT INTO Book VALUES (295837, 'Elephants', 2001, 285,  'African Publishing')
INSERT INTO Book VALUES (358329, 'Modern Art', 1988, 482,  'Belgian Publishing')
INSERT INTO Book VALUES (373811, 'Home Cooking', 2001, 420,  'Norway Publishers')
INSERT INTO Book VALUES (384721, 'Eric the Red', 2001, 276,  'Viking Publishers')
INSERT INTO Book VALUES (384839, 'Chemistry 201', 1954, 566,  'Rio Publishing')
INSERT INTO Book VALUES (386900, 'Raising Sheep', 2001, 375,  'Pacific Publishers')
INSERT INTO Book VALUES (426812, 'Personal Computers', 1994, 265,  'London Publishing Ltd')
INSERT INTO Book VALUES (445582, 'Party Time', 1956, 187,  'Norway Publishers')
INSERT INTO Book VALUES (471838, 'The Riviera', 1956, 421,  'Parisian Ltd')
INSERT INTO Book VALUES (482492, 'Paris at Night', 1933, 365,  'French Publishing')
INSERT INTO Book VALUES (483899, 'Tea Leaves', 1967, 335,  'Asian Publishers')
INSERT INTO Book VALUES (543823, 'French History', 1965, 490,  'Parisian Ltd')
INSERT INTO Book VALUES (558824, 'Steel Molding', 1999, 347,  'Kenya Publishers')
INSERT INTO Book VALUES (583938, 'Shearing Sheep', 2001, 258,  'Pacific Publishers')
INSERT INTO Book VALUES (584839, 'Asian History', 1984, 421,  'Asian Publishers')
INSERT INTO Book VALUES (638283, 'Biology 101', 1993, 632,  'Rio Publishing')
INSERT INTO Book VALUES (674283, 'Airplanes Today', 1995, 327,  'Belgian Publishing')
INSERT INTO Book VALUES (694737, 'Kenya History', 2001, 402,  'Kenya Publishers')
INSERT INTO Book VALUES (773342, 'Atlantic Days', 1999, 258,  'Rio Publishing')
INSERT INTO Book VALUES (842948, 'Calculators', 2001, 333,  'African Publishing')
INSERT INTO Book VALUES (853765, 'Working People', 1985, 385,  'London Publishing Ltd')
INSERT INTO Book VALUES (878721, 'Clocks and Watches', 1956, 368,  'Viking Publishers')
INSERT INTO Book VALUES (899333, 'Oriental Art', 1969, 377,  'Asian Publishers')
INSERT INTO Book VALUES (900326, 'French Cooking', 1992, 512,  'French Publishing')

INSERT INTO Writing VALUES (31732, 3818)
INSERT INTO Writing VALUES (245928, 3818)
INSERT INTO Writing VALUES (358329, 3818)
INSERT INTO Writing VALUES (384721, 4286)
INSERT INTO Writing VALUES (384839, 3800)
INSERT INTO Writing VALUES (386900, 3101)
INSERT INTO Writing VALUES (426812, 1484)
INSERT INTO Writing VALUES (426812, 2938)
INSERT INTO Writing VALUES (483899, 8294)
INSERT INTO Writing VALUES (584839, 4391)
INSERT INTO Writing VALUES (638283, 1203)
INSERT INTO Writing VALUES (899333, 6327)

INSERT INTO Sale VALUES (154299, 18384, '8/4/2005', 32.95, 1)
INSERT INTO Sale VALUES (295837, 16838, '10/12/2010', 28.99, 2)
INSERT INTO Sale VALUES (386900, 4838, '12/30/2010', 35.95, 1)
INSERT INTO Sale VALUES (426812, 4838, '5/11/2011', 25.5, 1)
INSERT INTO Sale VALUES (426812, 53719, '12/23/2009', 25.5, 2)
INSERT INTO Sale VALUES (471838, 32834, '2/22/2011', 43, 1)
INSERT INTO Sale VALUES (482492, 73402, '9/29/2011', 40, 3)
INSERT INTO Sale VALUES (543823, 73402, '4/14/2011', 20.99, 1)
INSERT INTO Sale VALUES (674283, 32834, '6/3/2010', 37.95, 1)
INSERT INTO Sale VALUES (899333, 32834, '9/30/2010', 59.95, 2)
INSERT INTO Sale VALUES (899333, 81477, '3/17/2009', 55.25, 1)



