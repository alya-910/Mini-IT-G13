from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from flask_login import login_required, current_user
from blueprints.messages import Notification

notifications = Blueprint('notifications', __name__)

# send notif
@notifications.route('/list')
def list_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).all()

    return render_template('notifications/notification_list.html', notifs=notifs)

# check if message has been read
@notifications.route('/read/<int:id>')
@login_required
def mark_as_read(id):
    notif = Notification.query.get_or_404(id)
    
    notif.is_read = True
    db.session.commit()

    if notif.link:
        return redirect(notif.link)

    return redirect(url_for('notifications.notification_list'))