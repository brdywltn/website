import requests, os, json
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime

#init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    #since the user_id is the PKey of our user table, use it in the query for the user
    return User.query.get(int(user_id))

###check the below link for some possiblee heelp on hte runtime error
#https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(1000))

# class TimestampMixin(object):
#     created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_title = db.Column(db.String(1000))
    post_content = db.Column(db.String(1000))


    

with app.app_context():
    print('creating all...')
    db.create_all()
    print('...success')
    

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html',
                                project_data=json_data) 

@app.route('/blog')
def blog():
    posts = Posts.query.all()
    return render_template('blog.html',
                                posts=posts)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    #login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    
    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.html'))
    
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

    

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    #code to validate and add user to database goes here
    #get username
    username = request.form.get('username')
    #get password
    password = request.form.get('password')

    #query db for username
    user = User.query.filter_by(username=username).first()

    if user: # if a user is found, redirect to signup page so they can try again
        flash('Username already exists')
        return redirect(url_for('signup'))

    #create a new user with the form data. Hash the password so the plaintext version isn't stored
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    #add the new user to the db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

#newpost
@app.route('/new_post')
@login_required
def new_post():
    return render_template('new_post.html')

@app.route('/new_post', methods=['POST'])
@login_required
def new_post_post():
    #title
    post_title = request.form.get('post_title')
    #content
    post_content = request.form.get('post_content')
    #create new post with the form data
    new_post = Posts(post_title=post_title, post_content=post_content)
    #add the post to the db
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('blog'))

#can split this out into a separate file - possibly with an abstracted
#get function that just passes a different query_url?
owner = 'broodj'
token = os.getenv('GITHUB_TOKEN')
query_url = f"https://api.github.com/users/{owner}/repos"
headers = {'Authorization': f'Bearer {token}', 
            'Accept': 'application/vnd.github+json'}
r = requests.get(query_url, headers=headers)
json_data = r.json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)