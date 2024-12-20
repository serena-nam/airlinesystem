#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
from hashlib import md5
from dateutil.relativedelta import relativedelta
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
	query = f'''SELECT *, 
		(
			SELECT AVG(rating) FROM reviews WHERE
			Flight.airline_name = airline_name and
			Flight.airplane_ID = airplane_ID and
			Flight.flight_num = flight_num and
			Flight.departure_date_time = departure_date_time
		) as avg_rating
 		FROM Flight WHERE 
		{ f'airline_name = "{airline_name}" and ' if airline_name else "" }
		{ f'departure_airport_code = "{departure_airport_code}" and ' if departure_airport_code else "" }
		{ f'arrival_airport_code = "{arrival_airport_code}" and ' if arrival_airport_code else "" }
		{ f'DATE(departure_date_time) >= "{date_range_begin}" and ' if date_range_begin else "" }
		{ f'DATE(arrival_date_time) <= "{date_range_end}" and ' if date_range_end else "" }
		'''
	if query.strip().split(' ')[-1] == 'and' or query.strip().split(' ')[-1] == 'WHERE':
		query = ' '.join(query.strip().split(' ')[:-1])
	query += ' ORDER BY departure_date_time DESC'
	cursor.execute(query)
	
	data = cursor.fetchall()
	cursor.close()

	#error message if no flights are found
	error = 'No Matching Flights'
	if data:
		return (1, data)
	else:
		return (0, error)


#Define a route to home function - goes to home page
@app.route('/')
def home():
	today = datetime.date.today().strftime("%Y-%m-%d")
	return render_template('/home.html', today=today)

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
	curDate = datetime.datetime.now()
	cursor = conn.cursor()

	query = '''SELECT * FROM purchases NATURAL JOIN flight 
	WHERE email=%s and departure_date_time > %s GROUP BY airline_name, airplane_ID, flight_num, departure_date_time'''
	print(f"Current session user: {session.get('username')}")
	cursor.execute(query, (email, curDate))
	future_data = cursor.fetchall()

	query = '''SELECT * FROM purchases NATURAL JOIN flight NATURAL LEFT OUTER JOIN reviews 
	WHERE email=%s and arrival_date_time < %s GROUP BY airline_name, airplane_ID, flight_num, departure_date_time'''
	cursor.execute(query, (email, curDate))
	past_data = cursor.fetchall()

	cursor.close()
	
	return render_template("customer/customer-home.html", future_flights=future_data, past_flights=past_data, name=name, email=email)
	

@app.route('/customer-find-flights') 
def customerFindFlights():
	today = datetime.date.today().strftime("%Y-%m-%d")
	return render_template('customer/customer-find-flights.html', today=today)

#finds flights for search in home page
@app.route('/findOpenFlights', methods=['POST'])
def findOpenFlights():
	#grabs information from the forms
	departure_airport_code = request.form.get('departure_airport_code')
	arrival_airport_code = request.form.get('arrival_airport_code')
	departure_date = request.form.get('departure_date')
	return_date = request.form.get('return_date')
 
	#cursor used to send queries only show queries where tickets can be purchased, show ticket price as adjusted
	cursor = conn.cursor()
	#executes query
	if(return_date):
		query = '''SELECT airline_name, airplane_ID, flight_num, departure_date_time, arrival_date_time, 
		departure_airport_code, arrival_airport_code, flight_status,
		ROUND(IF (num_seats*0.8 <= num_purchased, base_ticket_price*1.25, base_ticket_price),2) as ticket_price
		FROM 
		(SELECT airline_name, airplane_ID, flight_num, departure_date_time, 
		COUNT(*) as num_purchased from Purchases 
		GROUP BY airline_name, airplane_ID, flight_num, departure_date_time) as C 
		NATURAL JOIN Airplane NATURAL RIGHT OUTER JOIN Flight
		WHERE num_seats > num_purchased AND (departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(departure_date_time) = %s)
		OR 
		(departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(arrival_date_time) = %s)
		'''
		cursor.execute(query, (departure_airport_code, arrival_airport_code, departure_date, arrival_airport_code, departure_airport_code, return_date))
	else:
		query = '''SELECT airline_name, airplane_ID, flight_num, departure_date_time, arrival_date_time, 
		departure_airport_code, arrival_airport_code, flight_status,
		ROUND(IF (num_seats*0.8 <= num_purchased, base_ticket_price*1.25, base_ticket_price),2) as ticket_price
		FROM (SELECT airline_name, airplane_ID, flight_num, departure_date_time, 
		COUNT(*) as num_purchased FROM Purchases 
		GROUP BY airline_name, airplane_ID, flight_num, departure_date_time) as C 
		NATURAL JOIN Airplane NATURAL RIGHT OUTER JOIN Flight
		WHERE num_seats > num_purchased and departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(departure_date_time) = %s
		'''
		
		cursor.execute(query, (departure_airport_code, arrival_airport_code, departure_date))
	app.logger.debug(query)
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None

	#error message if no flights are found
	error = 'No Matching Flights'

	app.logger.info(data)

	today = datetime.date.today().strftime("%Y-%m-%d")
	if data:
		return render_template('customer/customer-find-flights.html', findFlights=data, today=today)
	else:
		return render_template('customer/customer-find-flights.html', error=error, today=today)

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
 		(departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(departure_date_time) = %s) OR (
 		departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(arrival_date_time) = %s)'''

		cursor.execute(query, (departure_airport_code, arrival_airport_code, departure_date, arrival_airport_code, departure_airport_code, return_date))
	else:
		query = '''SELECT * FROM Flight WHERE 
 		departure_airport_code = %s and
   		arrival_airport_code = %s and
		DATE(departure_date_time) = %s
	 	'''
		cursor.execute(query, (departure_airport_code, arrival_airport_code, departure_date))
	
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None

	#error message if no flights are found
	error = 'No Matching Flights'

	today = datetime.date.today().strftime("%Y-%m-%d")
	if data:
		return render_template("home.html", findFlights=data, today=today)
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
	cursor.execute(query, (email, md5(password.encode()).hexdigest()))
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
		session['role'] = 'customer'

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
		cursor.execute(ins, (fname, lname, email, md5(password.encode()).hexdigest(), building, street, apt, city, state, zipcode, passport, expiration, country, dob))
		conn.commit()

		insPhone = 'INSERT INTO customer_phone VALUES(%s, %s)'
		cursor.execute(insPhone, (email, phone))
		conn.commit()
		cursor.close()
		return render_template('customer/customer-login.html')

@app.route('/customer-purchase-ticket', methods=['GET', 'POST'])
def customerPurchase():
	if (not session) or(session['role'] != 'customer'):
		return render_template('/no-access.html')
	cursor = conn.cursor()
	return render_template('/customer/customer-purchase.html', flight=request.form)

@app.route('/purchaseTicket', methods=['GET', 'POST'])
def purchaseTicket():
	if (not session) or(session['role'] != 'customer'):
		return render_template('/no-access.html')
	email = session['username']
	cursor = conn.cursor()

	first_name = request.form['fname']
	last_name = request.form['lname']
	date_of_birth = request.form['dob']

	card_type = request.form['cardType']
	card_number = request.form['cardNum']
	card_name = request.form['cardName']
	card_expiration = request.form['expirationDate']

	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	flight_num = request.form['flight_num']
	departure_date_time = request.form['departure_date_time']
	ticket_price = request.form['ticket_price']
	
	#check for unclaimed ticket
	query = 'SELECT MAX(ticket_ID) as exist_ticket FROM ticket NATURAL LEFT OUTER JOIN purchases where airline_name=%s and airplane_ID=%s and flight_num=%s and departure_date_time=%s and email is NULL'
	cursor.execute(query, (airline_name, airplane_id, flight_num, departure_date_time));
	data = cursor.fetchone();
	if(data['exist_ticket']):
		ticket_id = data['exist_ticket']
	else:
		#create a new ticket with a new ticket_id
		query = 'SELECT COUNT(ticket_ID) as maxTicket FROM ticket'
		cursor.execute(query)
		conn.commit()
		data = cursor.fetchone()
		max_ticket = data['maxTicket'] if data['maxTicket'] else 0
		ticket_id = int(max_ticket) + 1

		ins = 'INSERT INTO ticket VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(ins, (ticket_id, airline_name, airplane_id, flight_num, departure_date_time))
		conn.commit()

	ins = 'INSERT INTO purchases VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	params = (email, ticket_id, airline_name, airplane_id, flight_num, departure_date_time, first_name, last_name, date_of_birth, ticket_price, card_type, card_number, card_expiration, card_name, datetime.datetime.today())
	cursor.execute(ins, params)
	conn.commit()

	return redirect(url_for("custHome"))

@app.route('/customer-cancel-ticket', methods=['POST'])
def customerCancel():
	if (not session) or(session['role'] != 'customer'):
		return render_template('/no-access.html')
	cursor = conn.cursor()
	email = session['username']

	ticket_id = request.form['ticket_id']
	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	flight_num = request.form['flight_num']
	departure_date_time = request.form['departure_date_time']

	first_name = request.form['fname']
	last_name = request.form['lname']

	query = 'DELETE FROM purchases WHERE email=%s and ticket_ID=%s and airline_name=%s and airplane_ID=%s and flight_num=%s and departure_date_time=%s and first_name=%s and last_name=%s'
	cursor.execute(query, (email, ticket_id, airline_name, airplane_id, flight_num, departure_date_time, first_name, last_name))
	conn.commit()
	return redirect('/customer-tickets')
	# return render_template('/customer/customer-tickets.html', flight=request.form)

@app.route('/customer-rate-flight', methods=['GET', 'POST'])
def customerReview():
	if (not session) or(session['role'] != 'customer'):
		return render_template('/no-access.html')
	cursor = conn.cursor()
	email = session['username']

	ticket_id = request.form['ticket_id']
	airline_name = request.form['airline_name']
	airplane_id = request.form['airplane_id']
	flight_num = request.form['flight_num']
	departure_date_time = request.form['departure_date_time']

	rating = request.form['rating']
	comment = request.form['comment']

	ins = 'INSERT INTO reviews VALUES(%s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(ins, (email, airline_name, airplane_id, flight_num, departure_date_time, rating, comment))
	conn.commit()
	return redirect(url_for('custHome'))


@app.route('/customer-tickets', methods=['GET', 'POST'])
def custTickets():
	if (not session) or(session['role'] != 'customer'):
		return render_template('/no-access.html')
	email = session['username']
	curDate = datetime.datetime.today()
	cursor = conn.cursor()

	query = 'SELECT * FROM purchases NATURAL JOIN flight WHERE email=%s ORDER BY departure_date_time DESC'
	print(f"Current session user: {session.get('username')}")
	cursor.execute(query, (email))
	data = cursor.fetchall()
	print(data)
	
	error = 'No Tickets Purchased'

	next_day = datetime.datetime.today() + datetime.timedelta(days=1)
	today = datetime.datetime.today()
	
	cursor.close()
	if data:
		return render_template('/customer/customer-tickets.html', flights=data, next_day=next_day, today=today)
	else:
		return render_template('/customer/customer-tickets.html', error=error)

@app.route('/customer-spending', methods=['GET', 'POST'])
def customerSpending():
	if (not session) or(session['role'] != 'customer'):
		return render_template('/no-access.html')
	cursor = conn.cursor()
 
	email = session['username']
	if request.method == 'POST':
		date_range_begin = request.form.get('date_range_begin')
		date_range_end = request.form.get('date_range_end')
	else:
		today = datetime.date.today()
		today_minus_1yr = (today - datetime.timedelta(days=365//2)).strftime('%Y-%m-%d')
		date_range_begin = str(today_minus_1yr)
		date_range_end = str(today)

	query = f'''SELECT SUM(ticket_price) as total FROM purchases WHERE 
 		email="{email}" and 
   		purchase_date_time >= "{date_range_begin}" and 
	 	purchase_date_time <= "{date_range_end}"
	'''
	cursor.execute(query)
	total = cursor.fetchone()['total']
	
	query = f'''SELECT DATE_FORMAT(purchase_date_time, '%m.%Y') as month, 
 		SUM(ticket_price) as total FROM purchases WHERE 
 		email="{email}" and 
   		purchase_date_time >= "{date_range_begin}" and 
	 	purchase_date_time <= "{date_range_end}"
		GROUP BY DATE_FORMAT(purchase_date_time, '%m.%Y')
	'''
	app.logger.debug(query)
	cursor.execute(query)
	app.logger.debug(query)
	spending_by_months = cursor.fetchall()
	if not spending_by_months:
		spending_by_months = []
  
	app.logger.debug(spending_by_months)

	# fill in missing months
	temp_date = date_range_begin
	if type(temp_date) is str:
		temp_date = datetime.datetime.strptime(temp_date, '%Y-%m-%d')
		temp_date = temp_date.replace(day=1)
	date_range_end_obj = datetime.datetime.strptime(date_range_end, '%Y-%m-%d')
	date_range_end_obj = date_range_end_obj.replace(day=1)
	complete_months = []
	while temp_date <= date_range_end_obj:
		complete_months.append(temp_date.strftime('%m.%Y'))
		temp_date = temp_date + relativedelta(months=1)
	
	spending_dict = {item['month']: item['total'] for item in spending_by_months}
	spending_by_months = [{'month': m, 'total': spending_dict.get(m, 0)} for m in complete_months]

	app.logger.debug(spending_by_months)
 
	cursor.close()	
	return render_template('/customer/customer-spending.html', total=total, months=spending_by_months, date_range_begin=date_range_begin, date_range_end=date_range_end)

	
@app.route('/staff-login')
def staffLogin():
	return render_template('staff/staff-login.html')

@app.route('/staff-register')
def staffRegister():
	cursor = conn.cursor()
	query = 'SELECT * FROM Airline'
	cursor.execute(query)
	airlines = cursor.fetchall()
	cursor.close()
	return render_template('staff/staff-register.html', airlines=airlines)

@app.route('/staff-home', methods=['GET', 'POST'])
def staffHome():
	app.logger.debug(session)
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')
	if request.method == 'POST':
		departure_airport_code = request.form.get('departure_airport_code')
		arrival_airport_code = request.form.get('arrival_airport_code')
		date_range_begin = request.form.get('date_range_begin')
		date_range_end = request.form.get('date_range_end')
	else:
		departure_airport_code = ''
		arrival_airport_code = ''
		date_range_begin = datetime.date.today().strftime('%Y-%m-%d')
		date_range_end = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
  
	(status, data) = filterFlights(session['airline'], departure_airport_code, arrival_airport_code, date_range_begin, date_range_end)
	if status:
		return render_template('staff/staff-home.html', flights=data, departure_airport_code=departure_airport_code, arrival_airport_code=arrival_airport_code, date_range_begin=date_range_begin, date_range_end=date_range_end)
	else:
		return render_template('staff/staff-home.html', error=data, departure_airport_code=departure_airport_code, arrival_airport_code=arrival_airport_code, date_range_begin=date_range_begin, date_range_end=date_range_end)

@app.route('/staff-customers-on-flight')
def staffCustomersOnFlight():
	if (not session) or(session['role'] != 'staff'):
		return render_template('/no-access.html')
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
	cursor.execute(query)
	customers = cursor.fetchall()
	
	cursor = conn.cursor()
	query = f'''SELECT * FROM reviews LEFT JOIN Customer on reviews.email = customer.email WHERE 
 		airline_name = "{airline_name}" and 
		airplane_ID = "{airplane_ID}" and 
		flight_num = "{flight_num}" and 
		departure_date_time = "{departure_date_time}"
		ORDER BY rating DESC
	'''
	cursor.execute(query)
	reviews = cursor.fetchall()
 
	cursor.close()
 
	return render_template('staff/staff-customers-on-flight.html', customers=customers, reviews=reviews)


@app.route('/staff-revenue', methods=['GET'])
def staffRevenue():
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')

	today_minus_1mo = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
	today_minus_1yr = (datetime.date.today() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

	cursor = conn.cursor()
 
	query = f'''SELECT sum(ticket_price) as total FROM purchases 
 		WHERE airline_name="{session['airline']}" and 
   		purchase_date_time >= "{today_minus_1mo}";
	'''
	cursor.execute(query)
	revenue_month = cursor.fetchone()['total']
 
	query = f'''SELECT sum(ticket_price) as total FROM purchases 
 		WHERE airline_name="{session['airline']}" and 
   		purchase_date_time >= "{today_minus_1yr}";
	'''
	cursor.execute(query)
	revenue_year = cursor.fetchone()['total']
 
	query = f'''SELECT 
			MONTH(purchase_date_time) as month, 
			count(*) as tickets,
			sum(ticket_price) as revenue
 		FROM purchases WHERE 
   		airline_name="{session['airline']}" and 
		purchase_date_time >= "{today_minus_1yr}" 
  		group by MONTHNAME(purchase_date_time);
	'''
	cursor.execute(query)
	tickets_by_month = cursor.fetchall()
 
	current_month = datetime.date.today().month
	month_indices = list(range(current_month, 13)) + list(range(1, current_month))
	month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	included_months = [t['month'] for t in tickets_by_month]
	for m in month_indices:
		if m not in included_months:
			tickets_by_month.append({'month': m, 'tickets': 0, 'revenue': 0})
	tickets_by_month = sorted(tickets_by_month, key=lambda x: month_indices.index(x['month']))
	tickets_by_month = [{'month': month_names[t['month']-1], 'tickets': t['tickets'], 'revenue': t['revenue']} for t in tickets_by_month]
 
	cursor.close()
	return render_template('staff/staff-revenue.html', revenue_month=revenue_month, revenue_year=revenue_year, tickets_by_month=tickets_by_month)



@app.route('/staff-add-new-airport', methods=["GET", "POST"])
def staffAddNewAirport():
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')
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
		try:
			cursor.execute(query)
			data = cursor.fetchone()
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
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')

	cursor = conn.cursor()
 
	# query = "SELECT * FROM Airplane WHERE airline_name=%s"
	cursor.execute(f'SELECT * FROM Airplane WHERE airline_name="{session["airline"]}"')
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
		try:
			cursor.execute(query)
			data = cursor.fetchone()
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


@app.route('/staff-add-new-maintenance', methods=["GET", "POST"])
def staffAddNewMaintenance():
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')

	cursor = conn.cursor()

	cursor.execute(f'SELECT DISTINCT airplane_ID FROM Airplane WHERE airline_name="{session["airline"]}"')
	airplanes = cursor.fetchall()
	airplane_IDs = [airplane['airplane_ID'] for airplane in airplanes]
	
	cursor.execute(f'SELECT * FROM Maintenance WHERE airline_name="{session["airline"]}"')
	maintenances = cursor.fetchall()
 
	if request.method == "POST":
		try:
			airline_name = session["airline"]
			airplane_ID = request.form.get('airplane_ID')
			start_date_time = request.form.get('start_date_time')
			end_date_time = request.form.get('end_date_time')
	
			# check for conflicting flights
			query = f'''SELECT flight_num FROM Flight WHERE
				airline_name="{airline_name}" and
				airplane_ID="{airplane_ID}" and
				flight_status!="cancelled" and
				(
					("{start_date_time}" BETWEEN departure_date_time and arrival_date_time) or
					("{end_date_time}" BETWEEN departure_date_time and arrival_date_time) or
					("{start_date_time}" < departure_date_time and "{end_date_time}" > arrival_date_time)
				)
			'''
			cursor.execute(query)
			flight_conflicts = cursor.fetchall()
			app.logger.debug(flight_conflicts)
			if flight_conflicts:
				raise Exception(f"Conflicts with existing flights: {[f['flight_num'] for f in flight_conflicts]}")

			# check for conflicting maintenance
			query = f'''SELECT COUNT(*) as conflicts FROM Maintenance WHERE
				airline_name="{airline_name}" and
				airplane_ID="{airplane_ID}" and
				(
					("{start_date_time}" BETWEEN start_date_time and end_date_time) or
					("{end_date_time}" BETWEEN start_date_time and end_date_time)
				)
			'''
			cursor.execute(query)
			maintenance_conflicts = cursor.fetchone()['conflicts']
			if maintenance_conflicts != 0:
				raise Exception("Conflicts with existing maintenance")
			
			query = f'''INSERT INTO Maintenance VALUES (
				"{airline_name}", "{airplane_ID}", "{start_date_time}", "{end_date_time}"
			)'''
   
			cursor.execute(query)
			data = cursor.fetchone()
			conn.commit()
						
			cursor.execute(f'SELECT * FROM Maintenance WHERE airline_name="{session["airline"]}"')
			maintenances = cursor.fetchall()
			cursor.close()
   
			return render_template('staff/staff-add-new-maintenance.html', maintenances=maintenances, airplane_IDs=airplane_IDs, status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-add-new-maintenance.html', maintenances=maintenances, airplane_IDs=airplane_IDs, error=str(e))
	else:
		return render_template('staff/staff-add-new-maintenance.html', maintenances=maintenances, airplane_IDs=airplane_IDs)


@app.route('/staff-add-new-flight', methods=["GET", "POST"])
def staffAddNewFlight():
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')

	cursor = conn.cursor()
 
	today = datetime.date.today().strftime('%Y-%m-%d')
	today_plus_30 = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
	(status, flights) = filterFlights(session["airline"], "", "", today, today_plus_30)
	if not status:
		flights = []
  
	cursor.execute("SELECT airplane_ID FROM Airplane WHERE airline_name=%s", (session["airline"]))
	airplanes = cursor.fetchall()
	airplane_IDs = [ airplane["airplane_ID"] for airplane in airplanes ]
	cursor.execute("SELECT airport_code FROM Airport")
	airports = cursor.fetchall()
	airports = [airport["airport_code"] for airport in airports]
	
	if request.method == "POST":
		try:
			airline_name = session["airline"]
			airplane_ID = request.form.get('airplane_ID')
			flight_num = request.form.get('flight_num')
			departure_date_time = request.form.get('departure_date_time')
			arrival_date_time = request.form.get('arrival_date_time')
			base_ticket_price = request.form.get('base_ticket_price')
			flight_status = request.form.get('flight_status')
			departure_airport_code = request.form.get('departure_airport_code')
			arrival_airport_code = request.form.get('arrival_airport_code')
	
			# check for conflicting maintenance
			if flight_status != 'cancelled':
				query = f'''SELECT COUNT(*) as conflicts FROM Maintenance WHERE
					airline_name="{airline_name}" and
					airplane_ID="{airplane_ID}" and
					(
						("{departure_date_time}" BETWEEN start_date_time and end_date_time) or
						("{arrival_date_time}" BETWEEN start_date_time and end_date_time)
					)
				'''
				cursor.execute(query)
				maintenance_conflicts = cursor.fetchone()['conflicts']
				if maintenance_conflicts != 0:
					raise Exception("Conflicts with scheduled maintenance")
 
			# check for conflicting flights
			query = f'''SELECT flight_num FROM Flight WHERE
				airline_name="{airline_name}" and
				airplane_ID="{airplane_ID}" and
				(
					("{departure_date_time}" BETWEEN departure_date_time and arrival_date_time) or
					("{arrival_date_time}" BETWEEN departure_date_time and arrival_date_time) or
					("{departure_date_time}" < departure_date_time and "{arrival_date_time}" > arrival_date_time)
				)
			'''
			cursor.execute(query)
			flight_conflicts = cursor.fetchall()
			if flight_conflicts:
				raise Exception(f"Conflicts with existing flights: {[f['flight_num'] for f in flight_conflicts]}")
			
			query = '''INSERT INTO Flight VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
		
			cursor.execute(query, (airline_name, airplane_ID, flight_num, departure_date_time, arrival_date_time, base_ticket_price, flight_status, departure_airport_code, arrival_airport_code))
			conn.commit()
			cursor.close()
			(status, flights) = filterFlights("", "", "", today, today_plus_30)
			if not status:
				flights = []
			return render_template('staff/staff-add-new-flight.html', airplane_IDs=airplane_IDs, airports=airports, flights=flights, status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-add-new-flight.html', airplane_IDs=airplane_IDs, airports=airports, flights=flights, error=str(e))
	else:
		return render_template('staff/staff-add-new-flight.html', airplane_IDs=airplane_IDs, airports=airports, flights=flights)
	
@app.route('/staff-change-flight-status', methods=['GET', 'POST'])
def staffChangeFlightStatus():
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')

	airline_name = request.args.get('airline_name')
	airplane_ID = request.args.get('airplane_ID')
	flight_num = request.args.get('flight_num')
	departure_date_time = request.args.get('departure_date_time')
	cursor = conn.cursor()
	query = f'''SELECT * FROM Flight WHERE
		airline_name="{airline_name}" and
		airplane_ID="{airplane_ID}" and
		flight_num="{flight_num}" and
		departure_date_time="{departure_date_time}"
	'''
	cursor.execute(query)
	flight = cursor.fetchone()
 
	if request.method == 'GET':
		cursor.close()
		return render_template('staff/staff-change-flight-status.html', flight=flight)
	else:
		new_status = request.form.get('new_status')
		try:
			cursor = conn.cursor()
			query = f'''UPDATE Flight SET flight_status="{new_status}" WHERE
				airline_name="{airline_name}" and
				airplane_ID="{airplane_ID}" and
				flight_num="{flight_num}" and
				departure_date_time="{departure_date_time}"
			'''
			cursor.execute(query)
			conn.commit()
   
			# get updated flight
			query = f'''SELECT * FROM Flight WHERE
				airline_name="{airline_name}" and
				airplane_ID="{airplane_ID}" and
				flight_num="{flight_num}" and
				departure_date_time="{departure_date_time}"
			'''
			cursor.execute(query)
			flight = cursor.fetchone()
   
			cursor.close()

			return render_template('staff/staff-change-flight-status.html', flight=flight, status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-change-flight-status.html', flight=flight, error=str(e))


@app.route('/staff-customer-lookup', methods=["GET", "POST"])
def staffCustomerLookup():
	if (not session) or (session['role'] != 'staff'):
		return render_template('/no-access.html')

	cursor = conn.cursor()
 
	today_minus_1yr = (datetime.date.today() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')

	queries = [f'''
 		CREATE VIEW Customer_freq AS SELECT Customer.email as email, COUNT(*) as freq 
 			FROM Purchases JOIN Customer ON Purchases.email=Customer.email
			WHERE airline_name="{session["airline"]}" and
			departure_date_time >= "{today_minus_1yr}"
	  		GROUP BY email;
		''', '''
		SELECT first_name, last_name, Customer.email, freq 
			FROM Customer JOIN Customer_freq ON Customer.email=Customer_freq.email
			WHERE freq=(SELECT max(freq) FROM Customer_freq);
		''', '''
		DROP VIEW Customer_freq;
		'''
	]
	cursor.execute(queries[0])
	cursor.execute(queries[1])
	frequent_customers = cursor.fetchall()
	cursor.execute(queries[2])
 
	if request.method == "POST":
		email = request.form.get('email')
		
		query = f'''SELECT *
			FROM (SELECT * FROM Flight where airline_name="{session["airline"]}") as F
			NATURAL JOIN (SELECT * FROM Purchases where email="{email}") as P
		'''
		try:
			cursor.execute(query)
			flights = cursor.fetchall()
			cursor.close()
			return render_template('staff/staff-customer-lookup.html', frequent_customers=frequent_customers, flights=flights, status="Success")
		except Exception as e:
			app.logger.error(e);
			return render_template('staff/staff-customer-lookup.html', frequent_customers=frequent_customers, flights=flights, error=str(e))
	else:
		return render_template('staff/staff-customer-lookup.html', frequent_customers=frequent_customers)



#Authenticates the customer login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	username = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()
	query = 'SELECT * FROM AirlineStaff WHERE username = %s and password = %s'
	cursor.execute(query, (username, md5(password.encode()).hexdigest()))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['first_name'] = data['first_name']
		session['role'] = 'staff'
		
		cursor = conn.cursor()
		query = 'SELECT airline_name FROM works WHERE username = %s'
		cursor.execute(query, (username))
		user_airline = cursor.fetchone()
		if user_airline:
			session['airline'] = user_airline['airline_name']
		else:
			session['airline'] = None
		cursor.close()
		app.logger.debug(session)
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
	airline_name = request.form['airline']
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
		cursor = conn.cursor()
		query = 'SELECT * FROM Airline'
		cursor.execute(query)
		airlines = cursor.fetchall()
		cursor.close()
		return render_template('staff/staff-register.html', airlines=airlines, error=error)
	else:
		insert_q = 'INSERT INTO AirlineStaff VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(insert_q, (username, md5(password.encode()).hexdigest(), fname, lname, dob))
		conn.commit()

		insert_email_q = 'INSERT INTO AirlineStaff_email VALUES(%s, %s)'
		cursor.execute(insert_email_q, (username, email))
		conn.commit()

		insert_phone_q = 'INSERT INTO AirlineStaff_phone VALUES(%s, %s)'
		cursor.execute(insert_phone_q, (username, phone))
		conn.commit()
  
		insert_works_q = 'INSERT INTO works VALUES(%s, %s)'
		cursor.execute(insert_works_q, (username, airline_name))
		conn.commit()
		cursor.close()
		return render_template('staff/staff-login.html')


#logout user(should work for both customer and staff)
@app.route('/logout')
def logout():
	old_role = session['role']
	session.clear()
	if old_role == 'staff':
		return redirect('/staff-login')
	else:
		return redirect('/customer-login')


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)

session.clear()