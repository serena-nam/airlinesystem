CREATE TABLE Airline(
	airline_name varchar(20),
	primary key (airline_name)
);
CREATE TABLE Airplane(
	airline_name varchar(20),
	airplane_ID varchar(20),
	num_seats int,
	manufacturing_company varchar(20),
	model_num varchar(20),
	manufacture_date date,
	primary key (airline_name, airplane_ID),
	foreign key (airline_name) references Airline (airline_name)
);
CREATE TABLE Maintenance(
	airline_name varchar(20),
	airplane_ID varchar(20),
	start_date_time datetime,
	end_date_time datetime,
	primary key (airline_name, airplane_ID, start_date_time, end_date_time),
	foreign key (airline_name, airplane_ID) references Airplane (airline_name, airplane_ID)
);
CREATE TABLE AirlineStaff(
	username varchar(20),
	password varchar(32),
	first_name varchar(20),
	last_name varchar(20),
	date_of_birth date,
	primary key (username)
);
CREATE TABLE AirlineStaff_phone(
	username varchar(20),
	phone_number varchar(10),
	primary key (username, phone_number),
	foreign key (username) references AirlineStaff(username)
);
CREATE TABLE AirlineStaff_email(
	username varchar(20),
	email varchar(50),
	primary key (username, email),
	foreign key (username) references AirlineStaff(username)
);
CREATE TABLE works(
	username varchar(20),
	airline_name varchar(20),
	primary key (username),
	foreign key (username) references AirlineStaff(username),
	foreign key (airline_name) references Airline(airline_name)
);
CREATE TABLE Airport(
	airport_code varchar(5),
	airport_name varchar(50),
	city varchar(20),
	country varchar(20),
	num_terminals int,
	airport_type varchar(20),
	primary key (airport_code)
);
CREATE TABLE Flight(
	airline_name varchar(20),
	airplane_ID varchar(20),
	flight_num varchar(10),
	departure_date_time datetime,
	arrival_date_time datetime,
	base_ticket_price decimal(10, 2),
	flight_status varchar(20),
    departure_airport_code varchar(5),
    arrival_airport_code varchar(5),
	primary key (airline_name, airplane_ID, flight_num, departure_date_time),
	foreign key (airline_name, airplane_ID) references Airplane(airline_name, airplane_ID),
    foreign key (departure_airport_code) references Airport(airport_code),
    foreign key (arrival_airport_code) references Airport(airport_code)
);
CREATE TABLE Ticket(
	ticket_ID varchar(20),
	airline_name varchar(20),
	airplane_ID varchar(20),
	flight_num varchar(10),
	departure_date_time datetime,
	primary key (ticket_ID, airline_name, airplane_ID, flight_num, departure_date_time),
	foreign key (airline_name, airplane_ID, flight_num, departure_date_time) references Flight(airline_name, airplane_ID, flight_num, departure_date_time)
);
CREATE TABLE Customer(
	first_name varchar(20),
	last_name varchar(20),
	email varchar(50),
	password varchar(32),
	building_name varchar(20),
	street_name varchar(20),
	apt_number varchar(10),
	city varchar(20),
	state varchar(2),
	zip_code varchar(10),
	passport_number varchar(20),
	passport_expiration date,
	passport_country varchar(20),
	date_of_birth date,
	primary key (email)
);
CREATE TABLE Customer_phone(
	email varchar(50),
	phone_number varchar(10),
	primary key (email, phone_number),
	foreign key (email) references Customer(email)
);
CREATE TABLE Purchases(
	email varchar(50),
	ticket_ID varchar(20),
	airline_name varchar(20),
	airplane_ID varchar(20),
	flight_num varchar(10),
	departure_date_time datetime,
	first_name varchar(20),
	last_name varchar(20),
	date_of_birth date,
	ticket_price decimal(10, 2),
	card_type varchar(20),
	card_number varchar(16),
	card_expiration_date date,
	card_name varchar(40),
	purchase_date_time datetime,
	primary key (email, ticket_ID, airline_name, airplane_ID, flight_num, departure_date_time),
	foreign key (email) references Customer(email),
	foreign key (ticket_ID, airline_name, airplane_ID, flight_num, departure_date_time) references Ticket(ticket_ID, airline_name, airplane_ID, flight_num, departure_date_time)
);
CREATE TABLE reviews(
    email varchar(50),
    airline_name varchar(20),
	airplane_ID varchar(20),
	flight_num varchar(10),
	departure_date_time datetime,
	rating int,
	comment varchar(500),
    primary key (email, airline_name, airplane_ID, flight_num, departure_date_time),
	foreign key (email) references Customer(email),
	foreign key (airline_name, airplane_ID, flight_num, departure_date_time) references Flight(airline_name, airplane_ID, flight_num, departure_date_time)
);