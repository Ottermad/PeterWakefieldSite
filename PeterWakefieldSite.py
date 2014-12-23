# Main file for Site

# Import statements

from datetime import datetime

import os

import sendgrid

import time

import markdown

import codecs

from werkzeug import secure_filename

from subprocess import Popen, PIPE

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    Markup,
    g,
)

from flask.ext.stormpath import (
    StormpathError,
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
    groups_required
)

# Constants
STORY_FOLDER = 'stories/'  # When deploying change to absolute path
DOCX_FOLDER = 'docxs/'
ALLOWED_EXTENSIONS = set(['txt', 'docx'])
URL = "http://127.0.0.1:5000/post/"

# App Settings
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'# comment out when deploying
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey-695ZMS0M2C6JBHX0W7G4UR9BI.properties'# When deploying change to absolute path
app.config['STORMPATH_APPLICATION'] = 'PeterWakefieldSite'
app.config['UPLOAD_FOLDER'] = DOCX_FOLDER

stormpath_manager = StormpathManager(app)

# Non-route functions

def get_key(a_list):
    return a_list[1]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_posts():
    posts = os.listdir(STORY_FOLDER)
    posts_with_time_from_epoch = []
    for post in posts:
        posts_with_time_from_epoch.append([post, os.path.getmtime(STORY_FOLDER + post)])
    sorted_posts = sorted(posts_with_time_from_epoch, key=get_key, reverse=True)
    return sorted_posts


# Routes

# Home page
@app.route('/')
def home():
    g.posts = get_posts()
    g.url = URL
    return render_template('home.html')

# Home page
@app.route('/about')
def about():
    g.posts = get_posts()
    g.url = URL
    return render_template('about.html')

# Contact page
@app.route('/contact')
def contact():
    g.posts = get_posts()
    g.url = URL
    return render_template('contact.html')

# Email Sender
@app.route('/send', methods=['POST'])
def send():
    sendgrid_object = sendgrid.SendGridClient("Ottermad", "OttersR0ck")
    message = sendgrid.Mail()
    sender = request.form["email"]
    subject = request.form["subject"]
    body = request.form["emailbody"]
    message.add_to("charlie.thomas@attwoodthomas.net")
    message.set_from(sender)
    message.set_subject(subject)
    message.set_html(body)

    sendgrid_object.send(message)
    flash('Email sent.')
    return redirect(url_for('contact'))

# Story listing page
@app.route('/stories')
def show_posts():
    g.posts = get_posts()
    g.url = URL
    return render_template('show_posts.html')

# Page for individual story
@app.route("/post/<name>")
def show_post(name):
    g.url = URL
    g.posts = get_posts()
    posts = get_posts()
    post = []
    post.append(name)
    pipe = Popen("w2m '{}{}'".format(STORY_FOLDER, post[0]), shell=True, stdout=PIPE).stdout
    markdown_content = pipe.read()
    html_content = markdown.markdown(markdown_content).translate({ord(k):None for k in u'`'})
    safe_html_content = Markup(html_content)
    post.append(safe_html_content)
    return render_template("post.html", post=post, posts=posts)

# Route for uploading Story
@app.route('/upload', methods=['GET', 'POST'])
@login_required
@groups_required(["Admins"])
def upload():
    g.url = URL
    g.posts = get_posts()
    # Check request method
    if request.method == 'POST':
        file = request.files['file']
        # Check if file is valid
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pipe = Popen("w2m '{}{}'".format(DOCX_FOLDER, filename), shell=True, stdout=PIPE).stdout
            output = pipe.read()
            print filename, DOCX_FOLDER
            new_filename = filename[:-5]
            fname = "{}{}.txt".format(STORY_FOLDER,new_filename)
            with open(fname, 'w') as fout:
                fout.write(output)
            return redirect(url_for('show_posts'))
    return render_template('upload.html')

# Login using stormpath
@app.route('/login', methods=['GET', 'POST'])
def login():
    g.url = URL
    g.posts = get_posts()
    error = None

    if request.method == 'POST':
        try:
            _user = User.from_login(
                request.form['email'],
                request.form['password'],
            )
            login_user(_user, remember=True)
            flash('You were logged in.')

            return redirect(url_for('show_posts'))
        except StormpathError, err:
            error = err.message

    return render_template('login.html', error=error)


# Logout route
@app.route('/logout')
def logout():
    g.url = URL
    g.posts = get_posts()
    logout_user()
    flash('You were logged out.')

    return redirect(url_for('show_posts'))


if __name__ == '__main__':
    app.run()
