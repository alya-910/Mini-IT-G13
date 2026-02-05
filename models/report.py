from extensions import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)

    reporter = db.relationship('User', foreign_keys=[reporter_id], backref='reports_made')
    reported_user = db.relationship('User', foreign_keys=[reported_user_id], backref='reports_received')
    listing = db.relationship('Item', backref='reports')