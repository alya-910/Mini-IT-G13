from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.user import User
from models.items import Item

users = Blueprint('user', __name__)

@users.route('/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    user_listings = Item.query.filter_by(seller_id=user.id).all()
    return render_template('account/profile.html', user=user, item=user_listings)

@users.route('/users')
@login_required
def user_list():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('users.html', users=users)