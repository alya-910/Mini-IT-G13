from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    
    # configure SQL Alchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['UPLOAD_FOLDER'] = 'static/profile_pics'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # import blueprints
    from routes.auth import auth
    from routes.account import account
    from routes.main import main

    # register bluepints
    app.register_blueprint(auth)
    app.register_blueprint(account)
    app.register_blueprint(main)

    return app

app = create_app()
        

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

