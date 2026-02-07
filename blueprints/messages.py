from flask import Blueprint, render_template, request, redirect, url_for
from models.message_model import ChatMessage
from extensions import db
from models.notification_model import Notification
from flask_login import login_required, current_user
from models.user import User

messages = Blueprint('messages', __name__)

# inbox
@messages.route('/chat')
@login_required
def inbox():
    messages = ChatMessage.query.filter_by(receiver_id = current_user.id).order_by(ChatMessage.timestamp.desc()).all()

    return render_template('messages/inbox.html', messages=messages)

# send messages
@messages.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        body = request.form.get('text')

        msg = ChatMessage(
            sender_id = current_user.id,
            receiver_id = other_user.id,
            body = body
        )

        db.session.add(msg)

        notif = Notification(
            user_id = other_user.id,
            message = f"New message from {current_user.username}",
            link = url_for('messages.chat', user_id=current_user.id)
        )

        db.session.add(notif)
        db.session.commit()

        return redirect(url_for('messages.chat', user_id=user_id))
    
    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_id == current_user.id) & (ChatMessage.receiver_id == user_id)) |
        ((ChatMessage.sender_id == user_id) & (ChatMessage.receiver_id == current_user.id))
    ).order_by(ChatMessage.timestamp.asc()).all()

    return render_template('messages/chat.html', messages=messages ,other_user=other_user)

# chats page
@messages.route('/chats')
@login_required
def chats():
    msgs = ChatMessage.query.filter(
        (ChatMessage.sender_id == current_user.id) | 
        (ChatMessage.receiver_id == current_user.id)
    ).order_by(ChatMessage.timestamp.desc()).all()

    user_ids = set()

    for msg in msgs:
        if msg.sender_id != current_user.id:
            user_ids.add(msg.sender_id)
        if msg.receiver_id != current_user.id:
            user_ids.add(msg.receiver_id)

    users = User.query.filter(User.id.in_(user_ids)).all()
    return render_template('messages/conversations.html', users=users)