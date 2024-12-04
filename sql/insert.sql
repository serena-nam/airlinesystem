/* 3 */
/* a */
INSERT into Airline VALUES("Jet Blue");

/* b */
INSERT into Airport VALUES("JFK","John F. Kennedy International Airport", "Queens", "USA", 5, "both");
INSERT into Airport VALUES("PVG","Shanghai Pudong International Airport", "Shanghai", "China", 2, "both");
INSERT into Airport VALUES("SFO", "San Francisco International Airport", "San Francisco", "USA", 4, "both");

/* c */
INSERT into Customer VALUES("Serena", "Nam", "sn3659@nyu.edu", "PlanePW123", "Carlyle Court", "25 Union Square W", "8B", "New York", "NY", 10003, "12345", "2030-01-01", "USA", "2005-08-31");
INSERT into Customer_phone VALUES("sn3659@nyu.edu", "6508625080");

INSERT into Customer VALUES("Brandon", "Kim", "bmk7319@nyu.edu", "myPW678", "Carlyle Court", "25 Union Square W", "20", "New York", "NY", 10003, "11111", "2031-09-01", "USA", "2004-11-15"); 
INSERT into Customer_phone VALUES("bmk7319@nyu.edu", "5302344565");

INSERT into Customer VALUES("Billy", "Joe", "billybobjoe@nyu.edu", "airplanePW!", "Othmer", "101 Johnson St.", "18","Brooklyn", "NY", 11201, "09876", "2027-11-05", "USA", "2003-12-25");
INSERT into Customer_phone VALUES("billybobjoe@nyu.edu", "7194414197");
INSERT into Customer_phone VALUES("billybobjoe@nyu.edu", "8412393112");

/* d */
INSERT into Airplane VALUES("Jet Blue", "B6015", 186, "Airbus", "A320", "2015-05-05");
INSERT into Airplane VALUES("Jet Blue", "B6616", 230, "Airbus", "A321", "2010-10-31");
INSERT into Airplane VALUES("Jet Blue", "B407", 125, "Airbus", "A317", "2017-01-17");

/* e */
INSERT into AirlineStaff VALUES("jk123", "staffPortalPW", "Jennifer", "Kazoo", "1987-06-03");
INSERT into AirlineStaff_phone VALUES("jk123", "2165945050");
INSERT into AirlineStaff_email VALUES("jk123", "kazoo63@hotmail.com");
INSERT into works VALUES("jk123", "Jet Blue");

/* f */
INSERT into Flight VALUES("Jet Blue", "B6015", "J6", "2024-11-10 08:20:00", "2024-11-10 15:55:00", 95.00, "delayed", "JFK", "SFO");
INSERT into Flight VALUES("Jet Blue", "B6616", "J17", "2024-10-29 22:15:00", "2024-10-30 05:20:00", 120.50, "on-time", "SFO", "JFK");
INSERT into Flight VALUES("Jet Blue", "B407", "J31", "2024-11-24 21:25:00", "2024-11-25 12:08:00", 110.00, "on-time", "JFK", "PVG");

/* g */
INSERT into Ticket VALUES("1", "Jet Blue", "B6015", "J6", "2024-11-10 08:20:00");
INSERT into Purchases VALUES("sn3659@nyu.edu", "1", "Jet Blue", "B6015", "J6", "2024-11-10 08:20:00", "Serena", "Nam", "2005-08-31", 95.00, "Visa", "1223458983653416", "2027-10-01", "Serena Nam", "2024-11-05 12:35:00");

INSERT into Ticket VALUES("2","Jet Blue", "B6015", "J6", "2024-11-10 08:20:00");
INSERT into Purchases VALUES("sn3659@nyu.edu", "2", "Jet Blue", "B6015", "J6", "2024-11-10 08:20:00", "Erin", "Nam", "2007-09-17", 95.00, "Visa", "1223458983653416", "2027-10-01", "Serena Nam", "2024-11-05 12:40:00");

INSERT into Ticket VALUES("3", "Jet Blue", "B407", "J31", "2024-11-24 21:25:00");
INSERT into Purchases VALUES("bmk7319@nyu.edu", "3", "Jet Blue", "B407", "J31", "2024-11-24 21:25:00", "Brandon", "Kim", "2004-11-15", 110.00, "Mastercard", "5763292187213283", "2028-09-01", "Minsoo Kim", "2024-07-26 21:27:21");

INSERT into Ticket VALUES("4", "Jet Blue", "B6616", "J17", "2024-10-29 22:15:00");
INSERT into Purchases VALUES("billybobjoe@nyu.edu", "4", "Jet Blue", "B6616", "J17", "2024-10-29 22:15:00", "Billy", "Joe", "2004-10-27", 120.50, "American Express", "7239320384258948", "2031-03-01", "Billy Joe", "2024-07-26 21:27:21");
