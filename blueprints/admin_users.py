from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import User

admin_users_bp = Blueprint("admin_users", __name__, url_prefix="/admin/users")


def admin_only():
    return current_user.is_authenticated and current_user.role == "admin"


@admin_users_bp.before_request
def check_admin():
    if not admin_only():
        return redirect(url_for("view_listings"))


@admin_users_bp.route("/")
@login_required
def manage_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@admin_users_bp.route("/suspend/<int:user_id>")
@login_required
def suspend_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = "suspended"
    db.session.commit()
    return redirect(url_for("admin_users.manage_users"))


@admin_users_bp.route("/activate/<int:user_id>")
@login_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = "active"
    db.session.commit()
    return redirect(url_for("admin_users.manage_users"))


@admin_users_bp.route("/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_users.manage_users"))
