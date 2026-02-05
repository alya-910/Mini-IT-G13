from flask import Flask
from config import Config
from extensions import db, migrate, login_manager
from extensions import mail

# Import your blueprints
from blueprints.admin_users import admin_users_bp
from blueprints.admin_listings import admin_listings_bp
from blueprints.reports import reports_bp
from blueprints.auth_user import auth
from blueprints.account import account
from blueprints.main import main
from blueprints.messages import messages
from blueprints.notifications import notifications
from blueprints.users import users
from blueprints.item_listing import item
from blueprints.cart import cart

def create_app():
    # 1. Initialize the App
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. Initialize Extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # 3. Configure Login Manager
    login_manager.init_app(app)
    login_manager.login_view = "auth_user.login"

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4. Register Blueprints
    # app.register_blueprint(auth_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_listings_bp)

    app.register_blueprint(reports_bp)

    # alya's code
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(account, url_prefix="/account")
    app.register_blueprint(main)
    app.register_blueprint(messages, url_prefix="/messages")
    app.register_blueprint(notifications, url_prefix="/notifications")
    app.register_blueprint(users, url_prefix="/profile")

    # siti's code
    app.register_blueprint(item)
    app.register_blueprint(cart)

    return app

app = create_app()

# Only run if executed directly
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables if not exist
    app.run(debug=True)
