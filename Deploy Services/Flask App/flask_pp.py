# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:08:09 2020

@author: Théophile Louvart
"""
#Imports

import os


#Imports Flask Utilities

from flask import Flask, render_template, request, redirect, jsonify
#forms
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
#db
from flask_sqlalchemy import SQLAlchemy
#Manage login system import
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



#Security password import
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
#Other Imports
from datetime import datetime
import time


### KERAS UTILITIES 
from tensorflow.keras.models import load_model


### RD2F scripts
from rd2f_test_image import predict_image_class
from rd2f_get_last_images_deploy import get_last_image, get_list_cam
from rd2f_settings_deploy import RD2F_root


# Model saved with Keras model.save()
MODEL_PATH = 'models/rd2f_model.h5'
incrementation = 0

# Load trained model
model = load_model(MODEL_PATH)
model._make_predict_function()  


print('Model loaded. Check http://127.0.0.1:5000/')


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

class TestEntry(db.Model):
    #primary key means id always be unique
    id = db.Column(db.Integer, primary_key=True)
    #nullable means it has to be there
    cam_name = db.Column(db.String(100), nullable=False)
    prob =  db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(30), nullable=False, default='N/A')
    # default will put value if nothing
    state = db.Column(db.String(30), nullable=False,)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


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
    all_entry = TestEntry.query.order_by(TestEntry.date_posted)
    return render_template('dashboard.html', entries=all_entry, name = current_user.username)

@app.route('/dashboard/enable', methods=['GET','POST'])
def enable_s():

    choice = 65
    incrementation = len(TestEntry.query.all())
    path, name = get_last_image(RD2F_root, incrementation, choice)
    
    # Make prediction
    pred, class_pred = predict_image_class(model,path)

    
    #Edit Database
    new_entry = TestEntry(cam_name =name, prob=str(pred[0]), state=class_pred)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify(name = name)

@app.route('/dashboard/disable', methods=['GET','POST'])
def disable_s():
    return redirect('/dashboard')



@app.route('/posts',methods=['GET','POST'])
def posts():
        return render_template('posts.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        name = f.filename
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path)
        
        # Make prediction
        pred, class_pred = predict_image_class(model,file_path)
        result0 = [name,class_pred,str(pred[0]),class_pred]
        
        #Edit Database
        new_entry = TestEntry(cam_name =name, prob=str(pred[0]), state=class_pred)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify(result0)
    return None

@app.route('/delete_entry/<int:id>')
def delete_entry(id):
    entry = TestEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect('/dashboard')

if __name__ == "__main__":
    app.run(debug=True)