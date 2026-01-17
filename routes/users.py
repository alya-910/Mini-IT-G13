from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.message_model import Message
from database import db
from models.notification_model import Notification
from flask_login import login_required, current_user
from models.user import User

users = Blueprint('user', __name__)

@users.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('account/profile.html', user=user)

@users.route('/profile/users')
@login_required
def user_list():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('users.html', users=users)