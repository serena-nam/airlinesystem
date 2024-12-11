INSERT INTO Airline (airline_name) VALUES ('JetBlue');

INSERT INTO AirlineStaff (username, password, first_name, last_name, date_of_birth) 
VALUES ('admin', 'e2fc714c4727ee9395f324cd2e7f331f', 'Roe', 'Jones', '1978-05-25');

INSERT INTO AirlineStaff_phone (username, phone_number) 
VALUES ('admin', '1112223333'), ('admin', '4445556666');

INSERT INTO AirlineStaff_email (username, email) 
VALUES ('admin', 'staff1@nyu.edu'), ('admin', 'staff2@nyu.edu');

INSERT INTO works (username, airline_name) 
VALUES ('admin', 'JetBlue');

INSERT INTO Airplane (airline_name, airplane_ID, num_seats, model_num, manufacturing_company, manufacture_date) 
VALUES 
('JetBlue', '1', 4, 'B-101', 'Boeing', '2013-05-02'),
('JetBlue', '2', 4, 'A-101', 'Airbus', '2011-05-02'),
('JetBlue', '3', 50, 'B-101', 'Boeing', '2015-05-02');

INSERT INTO Maintenance (airline_name, airplane_ID, start_date_time, end_date_time) 
VALUES 
('JetBlue', '1', '2025-01-27 13:25:25', '2025-01-29 07:25:25'),
('JetBlue', '2', '2025-01-27 13:25:25', '2025-01-29 07:25:25');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, airport_type) 
VALUES 
('JFK', 'JFK', 'NYC', 'USA', 4, 'Both'),
('BOS', 'BOS', 'Boston', 'USA', 2, 'Both'),
('PVG', 'PVG', 'Shanghai', 'China', 2, 'Both'),
('BEI', 'BEI', 'Beijing', 'China', 2, 'Both'),
('SFO', 'SFO', 'San Francisco', 'USA', 2, 'Both'),
('LAX', 'LAX', 'Los Angeles', 'USA', 2, 'Both'),
('HKA', 'HKA', 'Hong Kong', 'China', 2, 'Both'),
('SHEN', 'SHEN', 'Shenzhen', 'China', 2, 'Both');

INSERT INTO Customer (email, password, first_name, last_name, building_name, street_name, city, state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth) 
VALUES 
('testcustomer@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Jon', 'Snow', '1555', 'Jay St', 'Brooklyn', 'NY', '', '54321', '2025-12-24', 'USA', '1999-12-19'),
('user1@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Alice', 'Bob', '5405', 'Jay Street', 'Brooklyn', 'NY', '', '54322', '2025-12-25', 'USA', '1999-11-19'),
('user2@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Cathy', 'Wood', '1702', 'Jay Street', 'Brooklyn', 'NY', '', '54323', '2025-10-24', 'USA', '1999-10-19'),
('user3@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 'Trudy', 'Jones', '1890', 'Jay Street', 'Brooklyn', 'NY', '', '54324', '2025-09-24', 'USA', '1999-09-19');

INSERT INTO Customer_phone (email, phone_number) 
VALUES 
('testcustomer@nyu.edu', '1234321'),
('user1@nyu.edu', '1234322'),
('user2@nyu.edu', '1234323'),
('user3@nyu.edu', '1234324');

INSERT INTO Flight (airline_name, flight_num, departure_airport_code, departure_date_time, arrival_airport_code, arrival_date_time, base_ticket_price, flight_status, airplane_ID) 
VALUES 
('JetBlue', '102', 'SFO', '2024-09-20 13:25:25', 'LAX', '2024-09-20 16:50:25', 300.00, 'on-time', '3'),
('JetBlue', '104', 'PVG', '2024-10-04 13:25:25', 'BEI', '2024-10-04 16:50:25', 300.00, 'on-time', '3'),
('JetBlue', '106', 'SFO', '2024-08-04 13:25:25', 'LAX', '2024-08-04 16:50:25', 350.00, 'delayed', '3'),
('JetBlue', '206', 'SFO', '2025-02-04 13:25:25', 'LAX', '2025-02-04 16:50:25', 400.00, 'on-time', '2'),
('JetBlue', '207', 'LAX', '2025-03-04 13:25:25', 'SFO', '2025-03-04 16:50:25', 300.00, 'on-time', '2'),
('JetBlue', '134', 'JFK', '2023-12-15 13:25:25', 'BOS', '2023-12-15 16:50:25', 300.00, 'delayed', '3'),
('JetBlue', '296', 'PVG', '2024-12-30 13:25:25', 'SFO', '2024-12-30 16:50:25', 3000.00, 'on-time', '1'),
('JetBlue', '715', 'PVG', '2024-09-28 10:25:25', 'BEI', '2024-09-28 13:50:25', 500.00, 'delayed', '1'),
('JetBlue', '839', 'SHEN', '2023-12-26 13:25:25', 'BEI', '2023-12-26 16:50:25', 300.00, 'on-time', '3');

INSERT INTO Ticket (ticket_ID, airline_name, flight_num, departure_date_time,airplane_ID) 
VALUES 
('1', 'JetBlue', '102', '2024-09-20 13:25:25', '3'),
('2', 'JetBlue', '102', '2024-09-20 13:25:25', '3'),
('3', 'JetBlue', '102', '2024-09-20 13:25:25', '3'),
('4', 'JetBlue', '104', '2024-10-04 13:25:25', '3'),
('5', 'JetBlue', '104', '2024-10-04 13:25:25', '3'),
('6', 'JetBlue', '106', '2024-08-04 13:25:25', '3'),
('7', 'JetBlue', '106', '2024-08-04 13:25:25', '3'),
('8', 'JetBlue', '839', '2023-12-26 13:25:25', '3'),
('9', 'JetBlue', '102', '2024-09-20 13:25:25', '3'),
('11', 'JetBlue', '134', '2023-12-15 13:25:25', '3'),
('12', 'JetBlue', '715', '2024-09-28 10:25:25', '1'),
('14', 'JetBlue', '206', '2025-02-04 13:25:25', '2'),
('15', 'JetBlue', '206', '2025-02-04 13:25:25', '2'),
('16', 'JetBlue', '206', '2025-02-04 13:25:25', '2'),
('17', 'JetBlue', '207', '2025-03-04 13:25:25', '2'),
('18', 'JetBlue', '207', '2025-03-04 13:25:25', '2'),
('19', 'JetBlue', '296', '2024-12-30 13:25:25', '1'),
('20', 'JetBlue', '296', '2024-12-30 13:25:25', '1');

INSERT INTO Purchases (email, ticket_ID, airline_name, airplane_ID, flight_num, departure_date_time, first_name, last_name, date_of_birth, ticket_price, card_type, card_number, card_expiration_date, card_name, purchase_date_time)
VALUES
('testcustomer@nyu.edu', '1', 'JetBlue', '3', '102', '2024-09-20 13:25:25', 'Jon', 'Snow', '1999-12-19', 300, 'credit', '1111222233334444', '2025-03-01', 'Jon Snow', '2024-08-17 11:55:55'),
('user1@nyu.edu', '2', 'JetBlue', '3', '102', '2024-09-20 13:25:25', 'Alice', 'Bob', '1999-11-19', 300, 'credit', '1111222233335555', '2025-03-01', 'Alice Bob', '2024-08-16 11:55:55'),
('user2@nyu.edu', '3', 'JetBlue', '3', '102', '2024-09-20 13:25:25', 'Cathy', 'Wood', '1999-10-19', 300, 'credit', '1111222233335555', '2025-03-01', 'Cathy Wood', '2024-09-14 11:55:55'),
('user1@nyu.edu', '4', 'JetBlue', '3', '104', '2024-10-04 13:25:25', 'Alice', 'Bob', '1999-11-19', 300, 'credit', '1111222233335555', '2024-03-01', 'Alice Bob', '2024-08-21 11:55:55'),
('testcustomer@nyu.edu', '5', 'JetBlue', '3', '104', '2024-10-04 13:25:25', 'Jon', 'Snow', '1999-12-19', 300, 'credit', '1111222233334444', '2024-03-01', 'Jon Snow', '2024-09-28 11:55:55'),
('testcustomer@nyu.edu', '6', 'JetBlue', '3', '106', '2024-08-04 13:25:25', 'Jon', 'Snow', '1999-12-19', 350, 'credit', '1111222233334444', '2024-03-01', 'Jon Snow', '2024-08-02 11:55:55'),
('user3@nyu.edu', '7', 'JetBlue', '3', '106', '2024-08-04 13:25:25', 'Trudy', 'Jones', '1999-09-19', 350, 'credit', '1111222233335555', '2024-03-01', 'Trudy Jones', '2024-07-23 11:55:55'),
('user3@nyu.edu', '8', 'JetBlue', '3', '839', '2023-12-26 13:25:25', 'Trudy', 'Jones', '1999-09-19', 300, 'credit', '1111222233335555', '2024-03-01', 'Trudy Jones', '2023-12-23 11:55:55'),
('user3@nyu.edu', '9', 'JetBlue', '3', '102', '2024-09-20 13:25:25', 'Trudy', 'Jones', '1999-09-19', 300, 'credit', '1111222233335555', '2024-03-01', 'Trudy Jones', '2024-07-14 11:55:55'),
('user3@nyu.edu', '11', 'JetBlue', '3', '134', '2023-12-15 13:25:25', 'Trudy', 'Jones', '1999-09-19', 300, 'credit', '1111222233335555', '2024-03-01', 'Trudy Jones', '2023-10-23 11:55:55'),
('testcustomer@nyu.edu', '12', 'JetBlue', '1', '715', '2024-09-28 10:25:25', 'Jon', 'Snow', '1999-12-19', 500, 'credit', '1111222233334444', '2024-03-01', 'Jon Snow', '2024-05-02 11:55:55'),
('user3@nyu.edu', '14', 'JetBlue', '2', '206', '2025-02-04 13:25:25', 'Trudy', 'Jones', '1999-09-19', 400, 'credit', '1111222233335555', '2024-03-01', 'Trudy Jones', '2024-11-20 11:55:55'),
('user1@nyu.edu', '15', 'JetBlue', '2', '206', '2025-02-04 13:25:25', 'Alice', 'Bob', '1999-11-19', 400, 'credit', '1111222233335555', '2024-03-01', 'Alice Bob', '2024-11-21 11:55:55'),
('user2@nyu.edu', '16', 'JetBlue', '2', '206', '2025-02-04 13:25:25', 'Cathy', 'Wood', '1999-10-19', 400, 'credit', '1111222233335555', '2024-03-01', 'Cathy Wood', '2024-09-19 11:55:55'),
('user1@nyu.edu', '17', 'JetBlue', '2', '207', '2025-03-04 13:25:25', 'Alice', 'Bob', '1999-11-19', 300, 'credit', '1111222233335555', '2024-03-01', 'Alice Bob', '2024-08-15 11:55:55'),
('testcustomer@nyu.edu', '18', 'JetBlue', '2', '207', '2025-03-04 13:25:25', 'Jon', 'Snow', '1999-12-19', 300, 'credit', '1111222233334444', '2024-03-01', 'Jon Snow', '2024-09-25 11:55:55'),
('user1@nyu.edu', '19', 'JetBlue', '1', '296', '2024-12-30 13:25:25', 'Alice', 'Bob', '1999-11-19', 3000, 'credit', '1111222233334444', '2024-03-01', 'Alice Bob', '2024-11-22 11:55:55'),
('testcustomer@nyu.edu', '20', 'JetBlue', '1', '296', '2024-12-30 13:25:25', 'Jon', 'Snow', '1999-12-19', 3000, 'credit', '1111222233334444', '2024-03-01', 'Jon Snow', '2023-12-17 11:55:55');

INSERT INTO reviews (email, airline_name, flight_num, departure_date_time, airplane_ID, rating, comment)
VALUES
('testcustomer@nyu.edu', 'JetBlue', '102', '2024-09-20 13:25:25', '3', 4, 'Very Comfortable'),
('user1@nyu.edu', 'JetBlue', '102', '2024-09-20 13:25:25', '3', 5, 'Relaxing, check-in and onboarding very professional'),
('user2@nyu.edu', 'JetBlue', '102', '2024-09-20 13:25:25', '3', 3, 'Satisfied and will use the same flight again'),
('testcustomer@nyu.edu', 'JetBlue', '104', '2024-10-04 13:25:25', '3', 1, 'Customer Care services are not good'),
('user1@nyu.edu', 'JetBlue', '104', '2024-10-04 13:25:25', '3', 5, 'Comfortable journey and Professional');
