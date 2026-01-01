from flask import Flask, redirect, url_for, render_template
from flask_login import login_required, current_user
from config import Config
from extensions import db, migrate, login_manager
from models import User, Listing, Message

# Import your blueprints
from blueprints.auth import auth_bp
from blueprints.admin_users import admin_users_bp
from blueprints.admin_listings import admin_listings_bp
from blueprints.reports import reports_bp

def create_app():
    # 1. Initialize the App
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. Initialize Extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 3. Configure Login Manager
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 4. Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_listings_bp)
    app.register_blueprint(reports_bp)

    # 5. Define Basic Routes directly on the app instance
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("view_listings"))
        return redirect(url_for("auth.login"))

    @app.route("/listings")
    @login_required
    def view_listings():
        listings = Listing.query.all()
        return render_template("listing_list.html", listings=listings)

    @app.route("/messages")
    @login_required
    def view_messages():
        # Get messages where the current user is the receiver
        messages = Message.query.filter_by(receiver_id=current_user.id).all()
        return render_template("messages.html", messages=messages)

    return app

# Only run if executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
