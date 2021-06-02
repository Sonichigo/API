from datetime import datetime, timedelta
from flask import Flask, request, make_response, session, flash,jsonify,render_template
from flask_mysqldb import MySQL
from flask_jwt_extended import jwt_required, get_jwt_identity
import MySQLdb.cursors
import os
import jwt

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = os.urandom(24)
app.config['MYSQL_HOST'] = 'api12192001.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'Asuna1219@api12192001'
app.config['MYSQL_PASSWORD'] = 'Asuna2001'
app.config['MYSQL_DB'] = 'user'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('C:/Users/KIIT/Desktop/API/templates/login.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response('Could Not verify',401)
	if request.method == 'POST' and 'username' in request.form and 'phonenumber' in request.form:
		username = request.form['username']
		number = request.form['phonenumber']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE name = %s AND phonenumber = %s', (username, number,))
		session['logged_in'] = True
		token=jwt.encode({
			'username': request.form['username'],
			'expiration': str(datetime.utcnow()+timedelta(seconds=120))
			})
		return jsonify({'token':token.decode('utf-8')})

if __name__ == '__main__':
	app.run(debug=True)