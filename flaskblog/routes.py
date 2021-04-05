#Author: Pranav Sastry
import os
import secrets
import sys
sys.path.append("/opt/anaconda3/lib/python3.7/site-packages/")
from flask import render_template,url_for,flash,redirect,request,abort
from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm,LoginForm,AccountForm,PostForm,UpdatePostForm,RequestResetForm,PasswordResetForm
from flaskblog import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
from PIL import Image
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1)
    posts = Post.query.order_by(Post.date.desc()).paginate(per_page=5)
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title="About")

@app.route("/register",methods=['GET','POST'])
def register():
    if(current_user.is_authenticated):
        return redirect("/home")
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
        return redirect("/home")
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

def save_picture(form_picture):
    rndm = secrets.token_hex(2)
    fname = current_user.username+"-"+rndm
    _,fname_ext = os.path.splitext(form_picture.filename)
    fname_with_ext = fname+fname_ext
    dir_path = os.path.join(app.root_path,'static/profile_pics')
    fname_path = os.path.join(app.root_path,'static/profile_pics',fname_with_ext)
    fname_path_without_ext = os.path.join(app.root_path,'static/profile_pics',fname)
    contents_of_dir = os.listdir(dir_path)
    for content in contents_of_dir:
        if(content.find(current_user.username)!=-1):
            os.remove(dir_path+"/"+content)
    size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(size)
    img.save(fname_path)
    return fname_with_ext

@app.route("/account",methods=['GET','POST'])
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
        return redirect(url_for('account'))
    elif request.method=="GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/{}'.format(current_user.image_file))
    return render_template('account.html',title="Account",image_file=image_file,form=form)

@app.route("/<username>/post/new",methods=['GET','POST'])
@login_required
def new_post(username):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created!","success")
        return redirect(url_for('home'))
    return render_template("new_post.html",title="New Post",form=form)

@app.route("/<username>/post/<id>")
def post_page(username,id):
    post = Post.query.filter_by(id=id).first()
    post_div_length = ((len(post.content)/3000)+1)*900
    return render_template("post_page.html",title="Post",post=post,post_div_length=post_div_length)

@app.route("/<username>/post/update/<id>",methods=['GET','POST'])
@login_required
def update_page(username,id):
    post = Post.query.filter_by(id=id).first()
    if(post is not None):
        if((post.author.username != current_user.username)):
            abort(403)
        elif(post.author.username!=username):
            abort(403)
        form = UpdatePostForm()
        if(form.validate_on_submit()):
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Post updated!","success")
            return redirect(url_for('post_page',username=post.author.username,id=post.id))
        elif(request.method=='GET'):
            form.title.data = post.title
            form.content.data = post.content
        return render_template("update_page.html",title="Update",post=post,form=form)
    else:
        flash("Post unavailable!")
        return redirect(url_for('home'))

@app.route("/<username>/post/delete/<id>")
@login_required
def delete_page(username,id):
    post = Post.query.filter_by(id=id).first()
    if(post is not None):
        if((post.author.username != current_user.username)):
            abort(403)
        elif(post.author.username!=username):
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!","success")
        return redirect("/home")
    else:
        flash("Post unavailable!")
        return redirect(url_for('home'))

@app.route("/<username>")
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

def send_email(user):
    GMAIL_BOT_UNAME = os.getenv("GMAIL_BOT_UNAME")
    GMAIL_BOT_PSWD = os.getenv("GMAIL_BOT_PSWD")
    msg = EmailMessage()
    msg['Subject'] = "Reset Password for {}".format(user.username)
    msg['From'] = ["Blog Server"]
    msg['To'] = ["{}".format(user.email)]
    token = user.get_reset_token()
    content = f'''To reset your password, visit the following link:
{url_for('reset_password',token=token,_external=True)}
If you didn't make this request, then kindly ignore!
                '''
    msg.set_content("{}".format(content))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_BOT_UNAME,GMAIL_BOT_PSWD)
        smtp.send_message(msg)
        smtp.quit()


@app.route("/reset_request",methods=['GET','POST'])
def reset_request():
    if(current_user.is_authenticated):
        logout_user()
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash("Email sent with instructions to reset password!","success")
        return redirect(url_for('login'))
    return render_template("reset_request.html",title="Reset Request",form=form)

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if(current_user.is_authenticated):
        logout_user()
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid/Expired token!")
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Password reset for {}!".format(user.username),"success")
        return redirect("/login")
    return render_template("reset_password.html",title="Reset Password",form=form)
