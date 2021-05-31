from flask import Flask, render_template, request, redirect, url_for, session, flash,json
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re
import os
import uuid
import random

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = os.urandom(24)
app.config['MYSQL_HOST'] = 'api12192001.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'Asuna1219@api12192001'
app.config['MYSQL_PASSWORD'] = 'Asuna2001'
app.config['MYSQL_DB'] = 'user'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

mysql = MySQL(app)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)