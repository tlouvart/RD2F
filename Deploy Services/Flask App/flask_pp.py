# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:08:09 2020

@author: Théophile Louvart
"""
#Imports
from flask import Flask, render_template, request, redirect
#DB import
from flask_sqlalchemy import SQLAlchemy

#Forms imports
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

#Security password import
from werkzeug.security import generate_password_hash, check_password_hash
  
#Manage login system import
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


from datetime import datetime

# Create a basic flask app
app =  Flask(__name__)

app.config['SECRET_KEY'] = "thisissecret"
# Tell flask app where db is stored
#Using sqlite before production deployement
# Sqlite store locally in file 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

Bootstrap(app)
# Link app and db
db = SQLAlchemy(app)


#Initiliasation of login management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Designing the db through class

class BlogPost(db.Model):
    #primary key means id always be unique
    id = db.Column(db.Integer, primary_key=True)
    #nullable means it has to be there
    title = db.Column(db.String(100), nullable=False)
    content =  db.Column(db.Text, nullable=False)
    # default will put value if nothing
    author = db.Column(db.String(30), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return 'Blog post' + str(self.id)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#Designing the login system
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])    
    remember = BooleanField('Remember me')
    
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email('Invalid Email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)]) 

#get cam name from txt
# d = []
# with open("list_cam_2020-08-13.txt") as f:
#     for line in f:
#         (key,val) = line.split()
#         d.append({'cam_name' : str(val)})



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username= form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(new_user)
        db.session.commit() 
        return "<h1> user created </h1>"
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/dashboard')
        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form) 

@app.route('/logout')
def log_out():
    logout_user() 
    return redirect('/')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name = current_user.username)



@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author= request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        #need to commit for permanent usage
        db.session.commit()

        return redirect('/posts')
    else :
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    del_post = BlogPost.query.get_or_404(id)
    db.session.delete(del_post)
    db.session.commit()

    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        edit_post = BlogPost.query.get_or_404(id)
        edit_post.title = request.form['title']
        edit_post.content = request.form['content']
        edit_post.author = request.form['author']
    
        #need to commit for permanent usage
        db.session.commit()
        return redirect('/posts')
    return render_template('edit.html', post = BlogPost.query.get_or_404())



if __name__ == "__main__":
    app.run(debug=True)