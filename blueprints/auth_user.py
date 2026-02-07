from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from extensions import db
from flask_login import login_user
from extensions import mail
from flask_mail import Message

auth = Blueprint('auth_user', __name__)

# user register route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form["password"]

        # check if password is long enough
        if len(password) < 6:
            flash("Password needs to be at least 6 characters", 'error')
            return redirect(url_for('auth_user.register'))

        # check if email is already in use
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already in use",'error')
            return redirect(url_for('auth_user.register'))
        
        #check if username is taken
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash("Username is taken", 'error')
            return redirect(url_for('auth_user.register'))
        
        # add new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        flash("Account created successfully!", 'success')
        return redirect(url_for('main.index'))
    
    return render_template('authentication/register.html')


# User log in route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        # check if email matches
        if not user:
            flash("Invalid email", 'error')
            return redirect(url_for('auth_user.login'))

        # check if password matches
        if not user.check_password(password):
            flash("Invalid password", 'error')
            return redirect(url_for('auth_user.login'))

        if user and user.check_password(password):
            login_user(user)
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('main.index'))

    return render_template('authentication/login.html')


# user log out
@auth.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", 'success')
    return redirect(url_for('main.index'))

# send mail for forgot password
def send_mail(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', recipients=[user.email])
    msg.body=f''' Click the link below to reset your password.

    {url_for('auth_user.reset_token', token=token, _external=True)}

    If you did not request this, please ignore this message.

    '''
    mail.send(msg)

# send email to request password reset
@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            send_mail(user)
            flash("Reset request sent. Check your email.", 'success')
            return redirect(url_for('auth_user.login'))
        
        else:
            flash("Invalid email. Please re-enter your email.", 'error')

    return render_template('authentication/forgot_password.html')


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_reset_token(token)

    if user is None:
        flash('The link is invalid or expired. Please retry', 'error')
        return redirect(url_for('auth_user.forgot_password'))
    
    if request.method == "POST":
        new_pw = request.form.get("new_password")
        confirm_pw = request.form.get("confirm_password")

        # check if password is long enough
        if len(new_pw) < 6:
            flash("Password needs to be at least 6 characters", 'error')
            return redirect(url_for('auth_user.reset_password'))
        
        # check if user entered the same password 
        if new_pw != confirm_pw:
            flash("New password and confirmation password do not match", 'error')
            return redirect(url_for('auth_user.reset_password'))

        user.set_password(new_pw)
        db.session.commit()
        
        flash("Password reset successfully. Please login.", 'success')
        return redirect(url_for('auth_user.login'))
    
    return render_template('authentication/reset_password.html', token=token)