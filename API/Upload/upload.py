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

mysql = MySQL(app)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        print(request.form['videotitle'])
        f_video = request.files['videofile']
        print(f_video.filename)
        # create video_url
        s3_bucket_video_url = <Main_Folder> + '/videos/' + video_file_name
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(
            f.filename, <BUCKET_NAME>,s3_bucket_video_url)
        return 'Success'
      
if __name__ == '__main__':
	app.run(debug=True)
