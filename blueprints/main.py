from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from models.items import Item
from models.message_model import ChatMessage

main = Blueprint('main', __name__)

@main.route('/')
def index():
    username = session.get('username')
    items = Item.query.all()
    return render_template("index.html", items=items)
