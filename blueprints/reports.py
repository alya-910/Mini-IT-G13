from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models.listing import Listing
from models.report import Report

reports_bp = Blueprint('reports', __name__)

# Route for users to submit a report
@reports_bp.route('/report/listing/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def report_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    if request.method == 'POST':
        reason = request.form.get('reason')
        details = request.form.get('details')
        
        new_report = Report(
            reason=reason,
            details=details,
            reporter_id=current_user.id,
            listing_id=listing.id,
            reported_user_id=listing.user_id
        )
        
        db.session.add(new_report)
        db.session.commit()
        
        flash('Report submitted successfully.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('report_form.html', listing=listing)

# Route for Admins to view all reports
@reports_bp.route('/admin/reports')
@login_required
def admin_reports():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))

    # ✅ FIXED: Removed 'admin/' path. Now it looks in the main templates folder.
    reports = Report.query.order_by(Report.timestamp.desc()).all()
    
    return render_template('reports.html', reports=reports)

# Route to delete/resolve a report
@reports_bp.route('/admin/reports/delete/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))
        
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    
    flash('Report resolved/deleted.', 'success')
    return redirect(url_for('reports.admin_reports'))