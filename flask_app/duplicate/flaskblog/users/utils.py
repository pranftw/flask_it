import os
import secrets
from PIL import Image
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from flask_login import current_user
from flask import url_for,current_app

def save_picture(form_picture):
    rndm = secrets.token_hex(2)
    fname = current_user.username+"-"+rndm
    _,fname_ext = os.path.splitext(form_picture.filename)
    fname_with_ext = fname+fname_ext
    dir_path = os.path.join(current_app.root_path,'static/profile_pics')
    fname_path = os.path.join(current_app.root_path,'static/profile_pics',fname_with_ext)
    fname_path_without_ext = os.path.join(current_app.root_path,'static/profile_pics',fname)
    contents_of_dir = os.listdir(dir_path)
    for content in contents_of_dir:
        if(content.find(current_user.username)!=-1):
            os.remove(dir_path+"/"+content)
    size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(size)
    img.save(fname_path)
    return fname_with_ext

def send_email(user):
    GMAIL_BOT_UNAME = os.getenv("GMAIL_BOT_UNAME")
    GMAIL_BOT_PSWD = os.getenv("GMAIL_BOT_PSWD")
    msg = EmailMessage()
    msg['Subject'] = "Reset Password for {}".format(user.username)
    msg['From'] = ["Blog Server"]
    msg['To'] = ["{}".format(user.email)]
    token = user.get_reset_token()
    content = f'''To reset your password, visit the following link:
{url_for('users.reset_password',token=token,_external=True)}
If you didn't make this request, then kindly ignore!
                '''
    msg.set_content("{}".format(content))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_BOT_UNAME,GMAIL_BOT_PSWD)
        smtp.send_message(msg)
        smtp.quit()
