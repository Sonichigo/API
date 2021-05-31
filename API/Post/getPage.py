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

@app.route('/getPage',methods=['GET'])
def getPage():
		#user = session.get('user')
		_user = '1'
		limit = pageLimit
		offset = request.form['offset']
		total_records = 0
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.callproc('sp_GetWishByUser',_user,limit,offset,total_records)
		wishes = cursor.fetchall()
		#cursor = cursor.execute("SELECT * FROM tbl_wish WHERE wish_user_id =%s", (_user))
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

if __name__ == '__main__':
	app.run(debug=True)