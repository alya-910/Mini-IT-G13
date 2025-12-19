from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models import Listing, Message, Report

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


# ---------- USER SIDE ----------

@reports_bp.route("/listing/<int:listing_id>", methods=["GET", "POST"])
@login_required
def report_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)

    if request.method == "POST":
        reason = request.form.get("reason")
        report = Report(
            report_type="listing",
            reason=reason,
            reporter_id=current_user.id,
            listing_id=listing.id,
        )
        db.session.add(report)
        db.session.commit()
        return redirect(url_for("view_listings"))

    return render_template("report_form.html", target_type="Listing", target=listing)


@reports_bp.route("/message/<int:message_id>", methods=["GET", "POST"])
@login_required
def report_message(message_id):
    message = Message.query.get_or_404(message_id)

    if request.method == "POST":
        reason = request.form.get("reason")
        report = Report(
            report_type="message",
            reason=reason,
            reporter_id=current_user.id,
            message_id=message.id,
        )
        db.session.add(report)
        db.session.commit()
        return redirect(url_for("view_messages"))

    return render_template("report_form.html", target_type="Message", target=message)


# ---------- ADMIN SIDE ----------

from flask_login import current_user  # ensure imported


def admin_only():
    return current_user.is_authenticated and current_user.role == "admin"


@reports_bp.route("/admin")
@login_required
def admin_reports():
    if not admin_only():
        return redirect(url_for("view_listings"))

    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template("admin_reports.html", reports=reports)


@reports_bp.route("/admin/<int:report_id>", methods=["GET", "POST"])
@login_required
def admin_report_detail(report_id):
    if not admin_only():
        return redirect(url_for("view_listings"))

    report = Report.query.get_or_404(report_id)

    if request.method == "POST":
        action = request.form.get("action")
        notes = request.form.get("admin_notes")

        report.admin_notes = notes
        report.status = "resolved"
        report.action_taken = action

        # Simple actions:
        if action == "suspend_listing" and report.listing:
            report.listing.status = "suspended"
        if action == "suspend_sender" and report.message:
            report.message.sender.status = "suspended"

        db.session.commit()
        return redirect(url_for("reports.admin_reports"))

    return render_template("admin_report_detail.html", report=report)
