from flask import Flask, render_template, request, redirect, url_for, session, flash,json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = os.urandom(24)
app.config['MYSQL_HOST'] = 'api12192001.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'Asuna1219@api12192001'
app.config['MYSQL_PASSWORD'] = 'Asuna2001'
app.config['MYSQL_DB'] = 'user'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

mysql = MySQL(app)

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'phonenumber' in request.form:
		username = request.form['username']
		number = request.form['phonenumber']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE name = %s AND phonenumber = %s', (username, number,))
		account = cursor.fetchone()
		if account: #wher user_id = token, 
			session['status'] = 1
			session['name'] = account['name']
			session['number'] = account['phonenumber']
			msg = 'Logged in successfully !'
			return render_template('userHome.html', msg = msg)
		else:
			msg = 'Incorrect Name / PhoneNumber!'
			return render_template('login.html', msg = msg)
	else:
		return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)