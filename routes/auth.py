from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user import User
from database import db

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
    
    return render_template('register.html')



# User log in route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main.home'))
        
        flash("Invalid email or password")
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.home'))