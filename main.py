import datetime
from time import localtime
from os import listdir
from os.path import isfile, join
import os 
import sqlite3
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Flask, request,Request ,session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug import SharedDataMiddleware
from subprocess import call

app = Flask(__name__) # create the application instance :)


# Create folders if they do not exist
if not os.path.exists('uploads'):
    os.mkdir('uploads')
if not os.path.exists('images'):
    os.mkdir('images')

#UPLOAD_FOLDER = 'upload/' 
''' ROSS ADDED THIS LINE 14:31 2018-12-20 '''
UPLOAD_FOLDER = 'uploads/' 
ALLOWED_EXTENSIONS = set(['csv','xls','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Clock(object):

    def refresh(self):
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
	self.loc = datetime.datetime.now()
	self.clocc = "{}:{}".format(self.hour,self.minute)
        if not self.day == 'Sunday' and not self.day == 'Saturday':
            if self.hour < 19 and self.hour > 8:
                if self.minute <= 49 and self.hour != 12:
                     return True
                else:
                    return False
		

		
        

        

   


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



@app.route('/')
def timecheck():
	return render_template('index.html')
		

@app.route('/files',methods = ['GET','POST'])
def upload():
	myvids = "/home/pi/devel/Daniel/FrontHCRaspberryPi/uploads/videos"
	onlyvids = [f for f in listdir(myvids) if isfile(join(myvids, f))]
	mypres = "/home/pi/devel/Daniel/FrontHCRaspberryPi/uploads/presentations"
	onlypres = [f for f in listdir(mypres) if isfile(join(mypres, f))]

	if request.method == 'POST':# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
			if file.filename == '':
				flash('No selected file')
			if file.filename.startswith("PRESENTATION"):
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(os.path.join('uploads/presentations', filename))
					return render_template('upload.html',filename=filename,vidlist = onlyvids,preslist=onlypres)			
			else:
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(os.path.join('uploads/videos', filename))
					return render_template('upload.html',filename=filename,vidlist = myvids,preslist=mypres)
	return render_template('upload.html',vidlist = myvids,preslist=mypres,clock = webclock)
	 
@app.route('/upload/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


	
	
if __name__ == "__main__":
    app.run(port=5000, debug=True,host="0.0.0.0")


	



