from time import localtime
import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Flask, request,Request ,session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

if not os.path.exists('uploads'):
    os.mkdir('uploads')

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
        self.hour = localtime()[3] - 7
        self.minute = localtime()[4]

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
        self.hour = localtime()[3] - 7
        self.minute = localtime()[4]

    def classtime(self):
        if self.minute <= 49 and self.hour != 12:
            return True
        else:
            return False

    def schoolday(self):
        if not self.day == 'Sunday' and not self.day == 'Saturday' \
            and self.hour < 19 and self.hour > 8:
            return True
        else:
            return False

    def update(self):
        self.refresh()
        if self.schoolday():
        	if self.classtime():
        		return 'classtime'
        	else:
        		return 'passing'



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
if webclock.update() == 'classtime':
    classtime()
elif webclock.update == 'passing':
    passing()
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

def connect_db():

    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')

def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/classtime')
def classtime():
	return render_template('classtime.html')
@app.route('/passing')
def passing():
	return render_template('passing.html')
@app.route('/uploads',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
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
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Herler! Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()





			



