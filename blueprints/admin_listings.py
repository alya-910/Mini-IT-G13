from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import Listing

admin_listings_bp = Blueprint("admin_listings", __name__, url_prefix="/admin/listings")


def admin_only():
    return current_user.is_authenticated and current_user.role == "admin"


@admin_listings_bp.before_request
def check_admin():
    if not admin_only():
        return redirect(url_for("view_listings"))


@admin_listings_bp.route("/")
@login_required
def manage_listings():
    listings = Listing.query.all()
    return render_template("admin_listings.html", listings=listings)


@admin_listings_bp.route("/toggle/<int:listing_id>")
@login_required
def toggle_status(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    listing.status = "suspended" if listing.status == "active" else "active"
    db.session.commit()
    return redirect(url_for("admin_listings.manage_listings"))


@admin_listings_bp.route("/delete/<int:listing_id>")
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    db.session.delete(listing)
    db.session.commit()
    return redirect(url_for("admin_listings.manage_listings"))
