from flask import Flask, redirect, url_for, render_template
from config import Config
from extensions import db, migrate, login_manager
from models import User

# Import your blueprints
# (You can keep your folder named 'blueprints' or rename it to 'routes' to match her)
from blueprints.auth import auth_bp
from blueprints.admin_users import admin_users_bp
from blueprints.admin_listings import admin_listings_bp
from blueprints.reports import reports_bp

def create_app():
    # 1. Create the App
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. Initialize Extensions (Connect them to the app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure Login Manager
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 3. Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_listings_bp)
    app.register_blueprint(reports_bp)

    # 4. Define Global Routes (Home page)
    @app.route("/")
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for("view_listings"))
        return redirect(url_for("auth.login"))

    return app

# Only run this if we are executing the file directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
