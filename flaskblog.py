#Author: Pranav Sastry
#DateTime: 2021-04-02 09:35:00.233711 IST

import sys
import os
sys.path.append("/opt/anaconda3/lib/python3.7/site-packages/")
import datetime as dt

from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '7606759b9c410f7865f82cd85bf75465'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return "User({},{},{},{})".format(self.id,self.username,self.email,self.image_file)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=dt.datetime.utcnow)
    title = db.Column(db.String(35),nullable=False)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return "Post({},{},{},{})".format(self.id,self.author,self.date,self.title)

posts = [{"author":"Pranav Sastry","title":"Hello World","content":"Crap","date":"23-12-2021","time":"23:33 IST"},
        {"author":"Pran Sastry","title":"Hello World","content":"Crap","date":"23-12-2021","time":"23:33 IST"},
        {"author":"Prani Sastry","title":"Hello World","content":"Crap","date":"23-12-2021","time":"23:33 IST"}]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title="About")

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {}!".format(form.username.data),"success")
        return redirect("/home")
    return render_template('register.html',title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.email.data=="admin@blog.com" and form.password.data=="password"):
            flash("Welcome {}".format(form.email.data),"success")
            return redirect("/home")
        else:
            flash("Login unsuccessful!","failure")
    return render_template('login.html',title="Login",form=form)

if __name__=='__main__':
    app.run(debug=True)
