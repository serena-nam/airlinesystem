#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='airline_system',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/customer-login')
def customer_login():
	return render_template('customer/customer-login.html')

@app.route('/customer-register')
def customer_register():
	return render_template('customer/customer-register.html')

@app.route('/customer-home')
def customer_home():
    # email = session['email']
    name = session['first_name']
    # cursor = conn.cursor();
    # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    # cursor.execute(query, (username))
    # data1 = cursor.fetchall() 
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
    return render_template('customer/customer-home.html', name=name)

@app.route('/getFlights', methods=['POST'])
def getFlights():
	#grabs information from the forms
	departure_airport_code = request.form.get('departure_airport_code')
	arrival_airport_code = request.form.get('arrival_airport_code')
	departure_date = request.form.get('departure_date')
 
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = '''SELECT * FROM Flight WHERE 
 		departure_airport_code = %s and
   		arrival_airport_code = %s and
		departure_date_time >= %s
     '''
	cursor.execute(query, (departure_airport_code, arrival_airport_code, departure_date))
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
		return render_template("home.html", flights=data)
	else:
		return render_template("home.html", error=error)


#Authenticates the customer login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
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
		session['email'] = email
		first_name = data['first_name']
		session['first_name'] = first_name

		return redirect(url_for('customer_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid email or password'
		return render_template('customer/customer-login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
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

		return render_template('customer/customer-home.html')



app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
