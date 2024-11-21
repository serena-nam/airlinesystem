#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='project',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('home.html')


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

	app.logger.info(data)
	if data:
		return render_template("yes.html", flights=data)
	else:
		return render_template("no.html")

		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
