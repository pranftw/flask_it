#Author: Pranav Sastry

from flask import render_template,url_for,flash,redirect,request
from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm,LoginForm
from flaskblog import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required

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
    if(current_user.is_authenticated):
        return redirect("\home")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {}!".format(form.username.data),"success")
        return redirect("/login")
    return render_template('register.html',title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if(current_user.is_authenticated):
        return redirect("\home")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if((user is not None) and (bcrypt.check_password_hash(user.password,form.password.data))):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Welcome back {}!".format(user.username),"success")
            return redirect(next_page) if next_page else redirect("/home")
        else:
            flash("Login unsuccessful!","failure")
    return render_template('login.html',title="Login",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/home")

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title="Account")
