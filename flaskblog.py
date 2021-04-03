#Author: Pranav Sastry
#DateTime: 2021-04-02 09:35:00.233711 IST

import sys
import os
sys.path.append("/opt/anaconda3/lib/python3.7/site-packages/")

from flask import Flask,render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '7606759b9c410f7865f82cd85bf75465'

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
    return render_template('login.html',title="Login",form=form)

if __name__=='__main__':
    app.run(debug=True)
