from flask import Blueprint,render_template,url_for,flash,redirect,request,abort
from flaskblog.models import User,Post
from flaskblog.users.forms import LoginForm,RegistrationForm,AccountForm,RequestResetForm,PasswordResetForm
from flask_login import login_user,current_user,logout_user,login_required
from flaskblog import bcrypt,db
from flaskblog.users.utils import save_picture,send_email

users = Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created for {}!".format(form.username.data),"success")
        return redirect(url_for('users.login'))
    return render_template('register.html',title="Register",form=form)

@users.route("/login",methods=['GET','POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if((user is not None) and (bcrypt.check_password_hash(user.password,form.password.data))):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Welcome back {}!".format(user.username),"success")
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login unsuccessful!","failure")
    return render_template('login.html',title="Login",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            fname_with_ext = save_picture(form.image_file.data)
            current_user.image_file = fname_with_ext
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!","success")
        return redirect(url_for('users.account'))
    elif request.method=="GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/{}'.format(current_user.image_file))
    return render_template('account.html',title="Account",image_file=image_file,form=form)

@users.route("/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    if(user is not None):
        image_file = url_for('static',filename='profile_pics/{}'.format(user.image_file))
        page = request.args.get('page',1)
        posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(per_page=5)
        return render_template("profile.html",image_file=image_file,user=user,posts=posts)
    else:
        image_file = url_for('static',filename='profile_pics/{}'.format('default.png'))
        page = request.args.get('page',1)
        posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(per_page=5)
        return render_template("profile.html",title="Profile",image_file=image_file,user=user,posts=posts)

@users.route("/reset_request",methods=['GET','POST'])
def reset_request():
    if(current_user.is_authenticated):
        logout_user()
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash("Email sent with instructions to reset password!","success")
        return redirect(url_for('users.login'))
    return render_template("reset_request.html",title="Reset Request",form=form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if(current_user.is_authenticated):
        logout_user()
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid/Expired token!")
        return redirect(url_for('users.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Password reset for {}!".format(user.username),"success")
        return redirect(url_for('users.login'))
    return render_template("reset_password.html",title="Reset Password",form=form)
