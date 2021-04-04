# Imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# config
app.config['SECRET_KEY'] = 'mysecret'

# Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
# 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
# Connect app to the db
Migrate(app, db)

# Login config
login_manager = LoginManager()
# pass app into login manager
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# Registering blueprints
from company_blog.error_pages.handlers import error_pages
from company_blog.core.views import core
from company_blog.users.views import users
from company_blog.blog_posts.views import blog_posts

app.register_blueprint(blog_posts)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
