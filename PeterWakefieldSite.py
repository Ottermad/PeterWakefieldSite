from datetime import datetime
import os
import time
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    Markup,
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

from werkzeug import secure_filename
UPLOAD_FOLDER = 'stories/'
ALLOWED_EXTENSIONS = set(['html'])

import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey-695ZMS0M2C6JBHX0W7G4UR9BI.properties'
app.config['STORMPATH_APPLICATION'] = 'PeterWakefieldSite'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

stormpath_manager = StormpathManager(app)

def get_key(a_list):
    return a_list[1]

@app.route('/')
def show_posts():
    posts = os.listdir("stories")
    posts_with_time_from_epoch = []
    for post in posts:
        posts_with_time_from_epoch.append([post, os.path.getmtime("stories/" + post)])
    sorted_posts = sorted(posts_with_time_from_epoch, key=get_key, reverse=True)

    return render_template('show_posts.html', posts=sorted_posts)

@app.route("/post/<name>")
def show_post(name):
    post = []
    post.append(name)
    with file("stories/" + name) as f:
        content = f.read()
        html_content = Markup(content)
        post.append(html_content)
    return render_template("post.html", post=post)

'''@app.route('/add_page')
def add_post_page():
    return render_template('add_post_page.html')'''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@groups_required(["Admins"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show_posts'))
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
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


@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')

    return redirect(url_for('show_posts'))


if __name__ == '__main__':
    app.run()
