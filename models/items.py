from extensions import db
from datetime import datetime

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    trade_option = db.Column(db.String(10))
    image_path = db.Column(db.String(200))
    seller_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)