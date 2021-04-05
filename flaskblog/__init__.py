#Author: Pranav Sastry

import sys
import os
sys.path.append("/opt/anaconda3/lib/python3.7/site-packages/")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    return app
