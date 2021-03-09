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
# 'sqlite:///' + os.path.join(basedir, 'data.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yufwbagekkpkbv:f5677c2e5e853e231bbdd46774342eed21ea32c70490f73b7feb38c76af744a5@ec2-54-161-239-198.compute-1.amazonaws.com:5432/d83ia1n0tib80'
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
