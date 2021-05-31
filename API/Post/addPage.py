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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method=='POST':
		file = request.files['file']
		extension =os.path.splitext(file.filename)[1]
		f_name = str(uuid.uuid4()) + extension
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],f_name))
		return json.dumps({'filename':f_name})

@app.route('/addPage',methods=['GET','POST'])
def addPage():
	if request.method == 'POST' and 'inputTitle' in request.form and 'inputDescription' in request.form:
		title = request.form['inputTitle']
		description = request.form['inputDescription']
		post_id = random.randrange(10)
		now = datetime.now()
		_user ='1'
		if request.form.get('filePath') is None:
			filepath = ''
		else:
			filepath = request.form.get('filePath')
		if request.form.get('done') is None:
			_done = 0
		else:
			_done = 1
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		#cursor.execute('INSERT INTO tbl_post(post_id,post_title, post_description,post_uploaded_path, post_user_id, post_date) VALUES (%s, %s, %s, %s, %s, %s)', (post_id,title, description,filepath,_user, now ))
		cursor.callproc('sp_addWish',(title,description,_user,filepath,_done))
		data = cursor.fetchall()
		if len(data) == 0:
			mysql.connection.commit()
			return redirect('/userHome')
        
	elif request.method=='POST':
		return render_template('error.html',error = 'An error occurred!')
		
	else:
		return render_template('addWish.html',error = 'Unauthorized Access')

if __name__ == '__main__':
	app.run(debug=True)