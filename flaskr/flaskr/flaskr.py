from time import localtime
import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Flask, request,Request ,session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug import SharedDataMiddleware

app = Flask(__name__) # create the application instance :)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Create folders if they do not exist
if not os.path.exists('uploads'):
    os.mkdir('uploads')
if not os.path.exists('images'):
    os.mkdir('images')

#UPLOAD_FOLDER = 'upload/' 
''' ROSS ADDED THIS LINE 14:31 2018-12-20 '''
UPLOAD_FOLDER = 'uploads/' 
ALLOWED_EXTENSIONS = set(['csv','xls','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Clock(object):

    def __init__(self):
        if localtime()[6] == 0:
            self.day = 'Monday'
        elif localtime()[6] == 1:
            self.day = 'Tuesday'
        elif localtime()[6] == 2:
            self.day = 'Wednesday'
        elif localtime()[6] == 3:
            self.day = 'Thursday'
        elif localtime()[6] == 4:
            self.day = 'Friday'
        elif localtime()[6] == 5:
            self.day = 'Satuday'
        elif localtime()[6] == 6:
            self.day = 'Sunday'
        else:
            pass
        self.hour = localtime()[3]
        self.minute = localtime()[4]
        if not self.day == 'Sunday' and not self.day == 'Saturday':
            if self.hour < 19 and self.hour > 8:
                if self.minute <= 49 and self.hour != 12:
                    self.classtime = True
                else:
                    self.classtime = False
		

		
        

        

   


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='rawesomesauce',
    USERNAME='sub2pewdiepie',
    PASSWORD='0-password'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


#Default place to go.
webclock = Clock()


"""
@app.route('/classtime')
def classtime():
	return render_template('classtime.html')
@app.route('/passing')
def passing():
	return render_template('passing.html')
"""

@app.route('/', methods = ['GET','POST'])
def upload():
	if request.method == 'POST':# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
			file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
			if file.filename == '':
				flash('No selected file')
				return redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				#return redirect(url_for('upload_file',filename=filename))
				return redirect(url_for('upload',filename=filename))
	return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Herler! Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/clock')
def time():
	return render_template('clock.html',clock=webclock)
if __name__ == "__main__":
    app.run(port=5000, debug=True,host="0.0.0.0")

			




