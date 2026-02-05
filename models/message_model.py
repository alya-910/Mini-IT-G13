from extensions import db
from datetime import datetime

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship(
        'User',
        foreign_keys=[sender_id],
        back_populates='sent_messages'
    )

    receiver = db.relationship(
        'User',
        foreign_keys=[receiver_id],
        back_populates='received_messages'
    )