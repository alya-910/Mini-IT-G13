from extensions import db

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # ✅ THIS IS THE MISSING LINE CAUSING YOUR ERROR:
    status = db.Column(db.String(50), default='active')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('listings', lazy=True))