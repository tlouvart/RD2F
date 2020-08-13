# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:08:09 2020

@author: Théophile Louvart
"""
#Imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a basic flask app
app =  Flask(__name__)

# Tell flask app where db is stored
#Using sqlite before production deployement
# Sqlite store locally in file 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# Link app and db
db = SQLAlchemy(app)

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



#get cam name from txt
d = []
with open("list_cam_2020-08-13.txt") as f:
    for line in f:
        (key,val) = line.split()
        d.append({'cam_name' : str(val)})



all_posts = [
    {
     'title': 'post 1',
     'content': 'first content of post 1',   
     'author' : 'Oui'
    },
    {
     'title': 'post 2',
     'content': 'first content of post 2 blblbl'    
    }
    ]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', posts=d)

@app.route('/home/<string:name>')
def hello(name):
    return "Hello, {}".format(name)

@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'you can only get this webpage'



if __name__ == "__main__":
    app.run(debug=True)