#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='airline_system',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)


def filterFlights(airline_name, departure_airport_code, arrival_airport_code, date_range_begin, date_range_end):
	cursor = conn.cursor()
	query = f'''SELECT * FROM Flight WHERE 
		{ f'airline_name = "{airline_name}" and ' if airline_name else "" }
		{ f'departure_airport_code = "{departure_airport_code}" and ' if departure_airport_code else "" }
		{ f'arrival_airport_code = "{arrival_airport_code}" and ' if arrival_airport_code else "" }
		{ f'DATE(departure_date_time) >= "{date_range_begin}" and ' if date_range_begin else "" }
		{ f'DATE(arrival_date_time) <= "{date_range_end}" and ' if date_range_end else "" }
		'''
	if query.strip().split(' ')[-1] == 'and' or query.strip().split(' ')[-1] == 'WHERE':
		query = ' '.join(query.strip().split(' ')[:-1])
	app.logger.debug(query)
	cursor.execute(query)
	
	data = cursor.fetchall()
	cursor.close()

	#error message if no flights are found
	error = 'No Matching Flights'
	app.logger.info(data)
	if data:
		return (1, data)
	else:
		return (0, error)


#Define a route to home function - goes to home page
@app.route('/')
def home():
	return render_template('/home.html')

#define a route to customerLogin function - goes to customer login page
@app.route('/customer-login')
def customerLogin():
	return render_template('customer/customer-login.html')

#define a route to customerRegister function - goes to customer reg page
@app.route('/customer-register')
def customerRegister():
	return render_template('customer/customer-register.html')

#define a route to custHome function - shows customer's homepage and their flights
@app.route('/customer-home')
def custHome():
	# email = session['email']
	name = session['first_name']
	email = session['username']
	curDate = datetime.date.today()
	cursor = conn.cursor()

	query = 'SELECT airline_name, airplane_ID, flight_num, departure_date_time, arrival_date_time FROM Customer NATURAL JOIN Flight WHERE email=%s and departure_date_time < %s'
	cursor.execute(query, (email, curDate))
	data = cursor.fetchall()
	cursor.close()
	error = 'No Upcoming Flights'
	app.logger.info(data)
	
	if data:
		return render_template("customer/customer-home.html", flights=data, name=name)
	else:
		return render_template("customer/customer-home.html", error=error)


#finds flights for search in home page
@app.route('/findFlights', methods=['POST'])
def findFlights():
	#grabs information from the forms
	departure_airport_code = request.form.get('departure_airport_code')
	arrival_airport_code = request.form.get('arrival_airport_code')
	departure_date = request.form.get('departure_date')
	return_date = request.form.get('return_date')
 
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if(return_date):
		query = '''SELECT * FROM Flight WHERE 
 		departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(arrival_date_time) = %s'''
		cursor.execute(query, (departure_airport_code, arrival_airport_code, return_date))
	else:
		query = '''SELECT * FROM Flight WHERE 
 		departure_airport_code = %s and
   		arrival_airport_code = %s and
		departure_date_time >= %s
	 	'''
		cursor.execute(query, (departure_airport_code, arrival_airport_code, departure_date))
	
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None

	#error message if no flights are found
	error = 'No Matching Flights'

	app.logger.info(data)
	if data:
		return render_template("home.html", findFlights=data)
	else:
		return render_template("home.html", error=error)

#shows status of flights in home page
@app.route('/checkStatus', methods=['POST'])
def checkStatus():
	#grabs information from the forms
	airline = request.form.get('airline_name')
	flight_num = request.form.get('flight_num')
	# departure_airport_code = request.form.get('departure_airport_code')
	# arrival_airport_code = request.form.get('arrival_airport_code')
	departure_date = request.form.get('departure_date')
	arrival_date = request.form.get('arrival_date')
 
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = '''SELECT * FROM Flight WHERE 
 		airline_name = %s and 
		flight_num = %s and
		DATE(departure_date_time) = %s
	 '''
	cursor.execute(query, (airline, flight_num, departure_date))
	# query = 'SELECT * FROM Flight'
	# cursor.execute(query)
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None

	#error message if no flights are found
	error = 'No Matching Flights'

	app.logger.info(data)
	if data:
		return render_template("home.html", checkFlights=data)
	else:
		return render_template("home.html", error=error)

#Authenticates the customer login
@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def custLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		first_name = data['first_name']
		session['first_name'] = first_name

		return redirect(url_for('custHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid email or password'
		return render_template('customer/customer-login.html', error=error)

#Authenticates the customer register
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def custRegisterAuth():
	#grabs information from the forms
	fname = request.form['fname']
	lname = request.form['lname']

	email = request.form['email']
	password = request.form['password']

	building = request.form['buildingName']
	street = request.form['streetName']
	apt = request.form['aptNum']

	city = request.form['city']
	state = request.form['state']
	zipcode = request.form['zipcode']

	phone = request.form['phone']
	passport = request.form['ppNum']
	expiration = request.form['ppExp']
	country = request.form['ppCountry']
	dob = request.form['dob']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer/customer-register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (fname, lname, email, password, building, street, apt, city, state, zipcode, passport, expiration, country, dob))
		conn.commit()

		insPhone = 'INSERT INTO customer_phone VALUES(%s, %s)'
		cursor.execute(insPhone, (email, phone))
		conn.commit()
		cursor.close()
		return render_template('customer/customer-login.html')


@app.route('/staff-login')
def staffLogin():
	return render_template('staff/staff-login.html')

@app.route('/staff-register')
def staffRegister():
	return render_template('staff/staff-register.html')

@app.route('/staff-home', methods=['GET', 'POST'])
def staffHome():
	if request.method == 'POST':
		departure_airport_code = request.form.get('departure_airport_code')
		arrival_airport_code = request.form.get('arrival_airport_code')
		date_range_begin = request.form.get('date_range_begin')
		date_range_end = request.form.get('date_range_end')
		app.logger.debug(departure_airport_code, arrival_airport_code)

	else:
		departure_airport_code = ''
		arrival_airport_code = ''
		date_range_begin = datetime.date.today().strftime('%Y-%m-%d')
		date_range_end = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
  
	(status, data) = filterFlights("", departure_airport_code, arrival_airport_code, date_range_begin, date_range_end)
	if status:
		return render_template('staff/staff-home.html', flights=data, departure_airport_code=departure_airport_code, arrival_airport_code=arrival_airport_code, date_range_begin=date_range_begin, date_range_end=date_range_end)
	else:
		return render_template('staff/staff-home.html', error=data, departure_airport_code=departure_airport_code, arrival_airport_code=arrival_airport_code, date_range_begin=date_range_begin, date_range_end=date_range_end)

@app.route('/staff-customers-on-flight')
def staffCustomersOnFlight():
	airline_name = request.args.get('airline_name')
	airplane_ID = request.args.get('airplane_ID')
	flight_num = request.args.get('flight_num')
	departure_date_time = request.args.get('departure_date_time')
	
	cursor = conn.cursor()
	query = f'''SELECT * FROM Purchases WHERE ticket_ID in (
		SELECT ticket_ID FROM Ticket WHERE
			airline_name = "{airline_name}" and 
			airplane_ID = "{airplane_ID}" and 
			flight_num = "{flight_num}" and 
			departure_date_time = "{departure_date_time}"
	)
	'''
	app.logger.debug(query)
	cursor.execute(query)
	
	data = cursor.fetchall()
	cursor.close()
 
	return render_template('staff/staff-customers-on-flight.html', customers=data)

@app.route('/staff-add-new-airport', methods=["GET", "POST"])
def staffAddNewAirport():
	if request.method == "POST":
		airport_code = request.form.get('airport_code').upper()
		name = request.form.get('name')
		city = request.form.get('city')
		country = request.form.get('country')
		num_terminals = request.form.get('num_terminals')
		airport_type = request.form.get('airport_type')
		
		cursor = conn.cursor()
		query = f'''INSERT INTO Airport VALUES (
			"{airport_code}", "{name}", "{city}", "{country}", {num_terminals}, "{airport_type}"
		)'''
		app.logger.debug(query)
		try:
			cursor.execute(query)
			data = cursor.fetchone()
			app.logger.debug(data)
			conn.commit()
			cursor.close()
			return render_template('staff/staff-add-new-airport.html', status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-add-new-airport.html', error=str(e))
	else:
		return render_template('staff/staff-add-new-airport.html')
	 

@app.route('/staff-add-new-airplane', methods=["GET", "POST"])
def staffAddNewAirplane():
	cursor = conn.cursor()
 
	# query = "SELECT * FROM Airplane WHERE airline_name=%s"
	cursor.execute(f'SELECT * FROM Airplane WHERE airline_name="{session["airline"]}"')
	# app.logger.debug(query)
	airplanes = cursor.fetchall()
	
	if request.method == "POST":
		airline_name = session["airline"]
		airplane_ID = request.form.get('airplane_ID')
		num_seats = request.form.get('num_seats')
		manufacturing_company = request.form.get('manufacturing_company')
		model_num = request.form.get('model_num')
		manufacture_date = request.form.get('manufacture_date')
		
		query = f'''INSERT INTO Airplane VALUES (
			"{airline_name}", "{airplane_ID}", {num_seats}, "{manufacturing_company}", "{model_num}", "{manufacture_date}"
		)'''
		app.logger.debug(query)
		try:
			cursor.execute(query)
			data = cursor.fetchone()
			app.logger.debug(data)
			conn.commit()
			
			cursor.execute(f'SELECT * FROM Airplane WHERE airline_name="{session["airline"]}"')
			airplanes = cursor.fetchall()
			cursor.close()
   
			return render_template('staff/staff-add-new-airplane.html', airplanes=airplanes, status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-add-new-airplane.html', airplanes=airplanes, error=str(e))
	else:
		return render_template('staff/staff-add-new-airplane.html', airplanes=airplanes)



@app.route('/staff-add-new-flight', methods=["GET", "POST"])
def staffAddNewFlight():
	cursor = conn.cursor()
 
	today = datetime.date.today().strftime('%Y-%m-%d')
	todayplus30 = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
	(status, flights) = filterFlights(session["airline"], "", "", today, todayplus30)
	if not status:
		flights = []
  
	cursor.execute("SELECT airplane_ID FROM Airplane WHERE airline_name=%s", (session["airline"]))
	airplanes = cursor.fetchall()
	airplane_IDs = [ airplane["airplane_ID"] for airplane in airplanes ]
	app.logger.debug(airplane_IDs)
	cursor.execute("SELECT airport_code FROM Airport")
	airports = cursor.fetchall()
	airports = [airport["airport_code"] for airport in airports]
	
	if request.method == "POST":
		airline_name = session["airline"]
		airplane_ID = request.form.get('airplane_ID')
		flight_num = request.form.get('flight_num')
		departure_date_time = request.form.get('departure_date_time')
		arrival_date_time = request.form.get('arrival_date_time')
		base_ticket_price = request.form.get('base_ticket_price')
		flight_status = request.form.get('flight_status')
		departure_airport_code = request.form.get('departure_airport_code')
		arrival_airport_code = request.form.get('arrival_airport_code')
		
		query = '''INSERT INTO Flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
	
		try:
			cursor.execute(query, (airline_name, airplane_ID, flight_num, departure_date_time, arrival_date_time, base_ticket_price, flight_status, departure_airport_code, arrival_airport_code))
			conn.commit()
			cursor.close()
			(status, flights) = filterFlights("", "", "", today, todayplus30)
			if not status:
				flights = []
			return render_template('staff/staff-add-new-flight.html', airplane_IDs=airplane_IDs, airports=airports, flights=flights, status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-add-new-flight.html', airplane_IDs=airplane_IDs, airports=airports, flights=flights, error=str(e))
	else:
		return render_template('staff/staff-add-new-flight.html', airplane_IDs=airplane_IDs, airports=airports, flights=flights)
	


#Authenticates the customer login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	username = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()
	query = 'SELECT * FROM AirlineStaff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		first_name = data['first_name']
		session['first_name'] = first_name
		
		cursor = conn.cursor()
		query = 'SELECT airline_name FROM works WHERE username = %s'
		cursor.execute(query, (username))
		user_airline = cursor.fetchone()['airline_name']
		cursor.close()
		session['airline'] = user_airline

		return redirect(url_for('staffHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid email or password'
		return render_template('staff/staff-login.html', error=error)


@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
	#grabs information from the forms
	fname = request.form['fname']
	lname = request.form['lname']
	dob = request.form['dob']
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	phone = request.form['phone']

	cursor = conn.cursor()
	query = 'SELECT * FROM AirlineStaff WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This username already exists"
		return render_template('customer/customer-register.html', error = error)
	else:
		insert_q = 'INSERT INTO AirlineStaff VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(insert_q, (username, password, fname, lname, dob))
		conn.commit()

		insert_email_q = 'INSERT INTO AirlineStaff_email VALUES(%s, %s)'
		cursor.execute(insert_email_q, (username, email))
		conn.commit()
  
		insert_phone_q = 'INSERT INTO AirlineStaff_phone VALUES(%s, %s)'
		cursor.execute(insert_phone_q, (username, phone))
		conn.commit()
		cursor.close()
		return render_template('staff/staff-login.html')



#logout user(should work for both customer and staff)
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
