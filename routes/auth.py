from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from database import db
from flask_login import login_user
from extensions import mail
from flask_mail import Message

auth = Blueprint('auth', __name__)

# user register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form["password"]

        # check if email is already in use
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already in use")
            return redirect(url_for('auth.register'))
        
        #check if username is taken
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Username is taken")
            return redirect(url_for('auth.register'))
        
        # add new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        flash("Account created successfully!")
        return redirect(url_for('main.home'))
    
    return render_template('authentication/register.html')



# User log in route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('main.home'))
        
        flash("Invalid email or password")
        return redirect(url_for('auth.login'))

    return render_template('authentication/login.html')

# user log out
@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('main.home'))

# forgot password
def send_mail(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', recipients=[user.email])
    msg.body=f''' Click the link below to reset your password.

    {url_for('auth.reset_token', token=token, _external=True)}

    If you did not request this, please ignore this message.

    '''
    mail.send(msg)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            send_mail(user)
            flash("Reset request sent. Check your email.")
            return redirect(url_for('auth.login'))
        
        else:
            flash("Invalid email. Please re-enter your email.")

    return render_template('authentication/forgot_password.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_reset_token(token)

    if user is None:
        flash('The link is invalid or expired. Please retry')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == "POST":
        new_pw = request.form.get("new_password")
        confirm_pw = request.form.get("confirm_password")

        if len(new_pw) < 6:
            flash("Password needs to be at least 6 characters")
            return redirect(url_for('auth.reset_password'))
        
        if new_pw != confirm_pw:
            flash("New password and confirmation password do not match")
            return redirect(url_for('auth.reset_password'))

        user.set_password(new_pw)
        db.session.commit()
        
        flash("Password reset successfully. Please login.")
        return redirect(url_for('auth.login'))
    
    return render_template('authentication/reset_password.html', token=token)