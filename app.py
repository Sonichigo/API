from flask import Flask, render_template, request, redirect, url_for, session, flash,json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import uuid

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MYSQL_HOST'] = 'api1219.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'Asuna1219@api1219'
app.config['MYSQL_PASSWORD'] = 'Asuna2001'
app.config['MYSQL_DB'] = 'USER'

mysql = MySQL(app)
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'phonenumber' in request.form:
		username = request.form['username']
		number = request.form['phonenumber']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = %s AND phonenumber = %s', (username, number))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('userHome.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'phonenumber' in request.form and 'email' in request.form :
		username = request.form['username']
		number = request.form['phonenumber']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
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
			cursor.execute('INSERT INTO user VALUES (%s, %s, %s)', (username, number, email))
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



@app.route('/addWish',methods=['GET','POST'])
def add():
	return render_template('addWish.html')
def addWish():
		if request.method == 'POST' and 'inputTitle' in request.form and 'inputDescription' in request.form:
			_title = request.form['inputTitle']
			_description = request.form['inputDescription']
			_user = session.get('user')
			datetime = os.datetime.now
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO tbl_post VALUES (%s, %s, %s, %s)', (_title, _description, _user, datetime))
			mysql.connection.commit()
			mysql.connection.close()
			msg=''
			msg='Published successfully!'
			return redirect('/userHome',msg=msg)
        
		else:
			return render_template('error.html',error = 'An error occurred!')

if __name__ == '__main__':
	app.run(debug=True)