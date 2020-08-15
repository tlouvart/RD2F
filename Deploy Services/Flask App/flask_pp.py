# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 19:08:09 2020

@author: Théophile Louvart
"""
#Imports
from flask import Flask, render_template, request, redirect
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
# d = []
# with open("list_cam_2020-08-13.txt") as f:
#     for line in f:
#         (key,val) = line.split()
#         d.append({'cam_name' : str(val)})



@app.route('/index')
def index():
    return render_template('index.html')

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