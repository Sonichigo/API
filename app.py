from flask import Flask, render_template, request, redirect, url_for, session, flash,json
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re
import os
import uuid
import random

app = Flask(__name__)

pageLimit =5

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = os.urandom(24)
app.config['MYSQL_HOST'] = 'api12192001.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'Asuna1219@api12192001'
app.config['MYSQL_PASSWORD'] = 'Asuna2001'
app.config['MYSQL_DB'] = 'user'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'phonenumber' in request.form:
		username = request.form['username']
		number = request.form['phonenumber']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE name = %s AND phonenumber = %s', (username, number,))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['name'] = account['name']
			session['number'] = account['phonenumber']
			msg = 'Logged in successfully !'
			return render_template('addWish.html', msg = msg)
		else:
			msg = 'Incorrect Name / PhoneNumber!'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/showDashboard')
def showDashboard():
    return render_template('dashboard.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'phonenumber' in request.form and 'email' in request.form :
		username = request.form['username']
		number = request.form['phonenumber']
		email = request.form['email']
		user_id = os.urandom(24)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE name = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not number or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO user.user VALUES (%s, %s, %s, %s)', (user_id,username, number, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
	
@app.route('/userHome')
def userHome():
        return render_template('userHome.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method=='POST':
		file = request.files['file']
		extension =os.path.splitext(file.filename)[1]
		f_name = str(uuid.uuid4()) + extension
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],f_name))
		return json.dumps({'filename':f_name})

@app.route('/addPage',methods=['GET','POST'])
def addWish():
	if request.method == 'POST' and 'inputTitle' in request.form and 'inputDescription' in request.form:
		title = request.form['inputTitle']
		description = request.form['inputDescription']
		user = session.get('name')
		if request.form.get('filePath') is None:
			filepath = ''
		else:
			filepath = request.form.get('filePath')
		if request.form.get('done') is None:
			_done = 0
		else:
			_done = 1
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		#cursor.execute('INSERT INTO tbl_post VALUES (%s, %s, %s, %s, %s, %s)', (post_id,title, description,_filepath, user,datetime ))
		cursor.callproc('sp_addWish',(title,description,user,filepath,_done))
		data = cursor.fetchall()
		if len(data) is 0:
			mysql.connection.commit()
			return redirect('/userHome')
        
	elif request.method=='POST':
		return render_template('error.html',error = 'An error occurred!')
		
	else:
		return render_template('addWish.html',error = 'Unauthorized Access')

@app.route('/showAddPage',methods=['GET','POST'])
def showAddWish():
	return render_template('addWish.html')

@app.route('/getPage',methods=['GET','POST'])
def getWish():
	if session.get('name'):
		user = session.get('user')
		limit = pageLimit
		offset = request.form['offset']
		total_records = 0
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.callproc('sp_GetWishByUser',(user,limit,offset))
		wishes = cursor.fetchall()
		cursor.execute('Select @sp_GetWishByUser')
		outParam = cursor.fetchall()
		response = []
		wishes_dict = []
		for wish in wishes:
			wish_dict = {
				'Id': wish[0],
				'Title': wish[1],
				'Description': wish[2],
				'Date': wish[4]}
			wishes_dict.append(wish_dict)
			response.append(wishes_dict)
			response.append({'total':outParam[0][0]})
		return json.dumps(response)
	else:
		return render_template('error.html',error = 'Unauthorized Access')

        
if __name__ == '__main__':
	app.run(debug=True)