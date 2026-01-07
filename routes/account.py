from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, logout_user
from models.user import User
from database import db
import uuid, os, time

account = Blueprint('account', __name__)

#route to account settings page
@account.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('account/dashboard.html', user=user, time_now=int(time.time()))

# update bio
@account.route('/update_bio', methods=['POST'])
@login_required
def update_bio():
    User.bio = request.form['bio']
    db.session.commit()
    flash("Bio updated!")
    return redirect(url_for('account.dashboard'))

# delete account
@account.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'GET':
        return render_template('account/confirm_delete.html', hide_navbar=True)

    choice = request.form.get("choice")

    if choice == "yes":
        user = User.query.get(session['user_id'])
        logout_user()
        db.session.delete(user)
        db.session.commit()
        flash("Account deleted.")
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('account.dashboard'))

# update profile
@account.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user = User.query.get(session['user_id'])

    # check if anythinf has been updated
    if request.method == 'POST':
        new_username = request.form.get("username")
        new_password = request.form.get("password_hash")
        new_bio = request.form.get("bio")
        new_profile_pic = request.files.get("profile_pic")
    
        # only update items with changes
        if new_username:
            user.username = new_username
        
        if new_password:
            user.password_hash = new_password

        if new_bio:
            user.bio = new_bio

        if new_profile_pic:
            pic_name = str(uuid.uuid1()) + "_" +(new_profile_pic.filename)
            filepath = os.path.join("static/profile_pics", pic_name)
            new_profile_pic.save(filepath)
            user.profile_pic = pic_name

        db.session.commit()
        flash("Profile updated successfully.")

    return redirect(url_for('account.dashboard'))

# change password
@account.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    user = User.query.get(session['user_id'])

    if request.method == "POST":
        current_pw = request.form.get("current_password")
        new_pw = request.form.get("new_password")
        confirm_pw = request.form.get("confirm_password")

        if not user.check_password(current_pw):
            flash("Current password is incorrect")
            return redirect(url_for('account.change_password'))

        if len(new_pw) < 6:
            flash("Password needs to be at least 6 characters")
            return redirect(url_for('account.change_password'))
        
        if new_pw != confirm_pw:
            flash("New password and confirmation password do not match")
            return redirect(url_for('account.change_password'))

        user.set_password(new_pw)
        db.session.commit()
        
        flash("Password changed successfully.")
        return redirect(url_for('account.dashboard'))

    return render_template("account/change_pwd.html")