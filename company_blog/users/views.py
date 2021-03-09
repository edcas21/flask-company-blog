from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from company_blog import db
from company_blog.models import User, BlogPost
from company_blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from company_blog.users.picture_handler import add_profile_pic

# Blueprint
users = Blueprint('users', __name__)

# Register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create new user object
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        # Add new user to the db
        db.session.add(user)
        db.session.commit()

        flash('Thank you for registering!')

        return redirect(url_for('users.login'))

    return render_template('register.html', form = form)

# Login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    # If form is valid upon submission
    if form.validate_on_submit():

        # Grab user tuple by the email entered
        user = User.query.filter_by(email=form.email.data).first()

        # If the user exists, check the password
        if user.check_password(form.password.data) and user is not None:

            # login the user
            login_user(user)
            flash('Log in Successful!')

            # Redirect them to the page they are trying to access
            next = request.args.get('next')

            # If not any other page than just redirect them to the home page
            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)
        else:
            return redirect(url_for('users.login'))

    return render_template('login.html', form = form)

# Logout
@users.route('/logout')
def logout():
    logout_user()
    # Redirect user back to home
    return redirect(url_for('core.index'))

# Account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
         # Check if the user is trying to upload a picture
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')

        return redirect(url_for('users.account'))

    # If there's no submission of new information, just get their current info
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image = profile_image, form = form)


# user's list of Blog posts
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page = page, per_page = 6)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
