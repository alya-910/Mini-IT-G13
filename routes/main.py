from flask import Blueprint, render_template, session

main = Blueprint('main', __name__)

@main.route('/')
def home():
    username = session.get('username')
    return render_template('home.html', username=username)