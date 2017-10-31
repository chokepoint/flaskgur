""" Main view definitions.
"""
import time
import os
import sqlite3
from hashlib import md5
from PIL import Image

from flask import request, g, redirect, url_for, abort, render_template, send_from_directory
from werkzeug.utils import secure_filename
from . import app


def check_extension(extension):
    """
    Make sure extension is in the ALLOWED_EXTENSIONS set
    """
    return extension in app.config['ALLOWED_EXTENSIONS']

def connect_db():
    """ Connect to the SQLite database.
    """
    query = open(app.config['SCHEMA'], 'r').read()
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    cursor.executescript(query)
    conn.commit()
    cursor.close()
    return sqlite3.connect(app.config['DATABASE'])

def get_last_pics():
    """ Return a list of the last 25 uploaded images
    """
    cur = g.db.execute('select filename from pics order by created_on desc limit 25')
    filenames = [row[0] for row in cur.fetchall()]
    return filenames


def add_pic(filename):
    """ Insert filename into database
    """
    g.db.execute('insert into pics (filename) values (?)', [filename])
    g.db.commit()

def gen_thumbnail(filename):
    """ Generate thumbnail image
    """
    height = width = 200
    original = Image.open(os.path.join(app.config['UPLOAD_DIR'], filename))
    thumbnail = original.resize((width, height), Image.ANTIALIAS)
    thumbnail.save(os.path.join(app.config['UPLOAD_DIR'], 'thumb_'+filename))


@app.before_request
def before_request():
    """ Executes before each request.
    Taken from flask example app
    """
    g.db = connect_db()


@app.teardown_request
def teardown_request(err):
    """ Executes after each request, regardless of whether
    there was an exception or not.
    """
    if err:
        app.logger.info(err.message)
    database = getattr(g, 'db', None)
    if database is not None:
        database.close()

@app.errorhandler(404)
def page_not_found(err):
    """ Redirect to 404 on error.
    """
    if err:
        app.logger.info(err.message)
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def upload_pic():
    """ Default route.
    """
    if request.method == 'POST':
        image_file = request.files['file']
        try:
            extension = image_file.filename.rsplit('.', 1)[1].lower()
        except IndexError, err:
            app.logger.info(err.message)
            abort(404)
        if image_file and check_extension(extension):
            # Salt and hash the file contents
            filename = md5(image_file.read() +
                           str(round(time.time() * 1000))
                          ).hexdigest() + '.' + extension
            image_file.seek(0) # Move cursor back to beginning so we can write to disk
            image_file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            add_pic(filename)
            gen_thumbnail(filename)
            return redirect(url_for('show_pic', filename=filename))
        else: # Bad file extension
            abort(404)
    else:
        return render_template('upload.html', pics=get_last_pics())

@app.route('/show')
def show_pic():
    """ Show a file specified by GET parameter.
    """
    filename = request.args.get('filename', '')
    return render_template('upload.html', filename=filename)

@app.route('/pics/<filename>')
def return_pic(filename):
    """ Show just the image specified.
    """
    return send_from_directory(app.config['UPLOAD_DIR'], secure_filename(filename))
