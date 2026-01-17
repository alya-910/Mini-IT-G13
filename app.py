from flask import Flask
from database import db
from flask_login import LoginManager
from extensions import mail

def create_app():
    app = Flask(__name__)

    
    # configure SQL Alchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mmu-thriftwize'
    app.config['UPLOAD_FOLDER'] = 'static/profile_pics'

    # email configuration
    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = '36df090f947a3e'
    app.config['MAIL_PASSWORD'] = '50704eb8222b6e'
    app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@thriftwize.com'

    db.init_app(app)
    mail.init_app(app)

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
    from routes.messages import messages
    from routes.notifications import notifications
    from routes.users import users

    # register bluepints
    app.register_blueprint(auth)
    app.register_blueprint(account)
    app.register_blueprint(main)
    app.register_blueprint(messages)
    app.register_blueprint(notifications)
    app.register_blueprint(users)

    return app

app = create_app()
        

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

