from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from models.items import Item
from models.items import Item
from models.message_model import ChatMessage

main = Blueprint('main', __name__)

@main.route('/')
def index():
    username = session.get('username')
    items = Item.query.all()
    return render_template("index.html", items=items)

@main.route("/listings")
@login_required
def view_listings():
    listings = Item.query.all()
    return render_template("listing_list.html", listings=listings)

@main.route("/messages")
@login_required
def view_messages():
    # Get messages where the current user is the receiver
    messages = ChatMessage.query.filter_by(receiver_id=current_user.id).all()
    return render_template("messages.html", messages=messages)