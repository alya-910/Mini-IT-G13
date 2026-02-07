from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

# database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.Text, default="")
    profile_pic = db.Column(db.String(200), default="default.jpg")

    role = db.Column(db.String(50), default='user')
    status = db.Column(db.String(50), default='active')

    sent_messages = db.relationship(
    'ChatMessage',
    foreign_keys='ChatMessage.sender_id',
    back_populates='sender'
)

    received_messages = db.relationship(
        'ChatMessage',
        foreign_keys='ChatMessage.receiver_id',
        back_populates='receiver'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
        except:
            return None
        return User.query.get(data['user_id'])

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"