import os
from flask import Blueprint, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from extensions import db
from models.items import Item
from flask import current_app
from flask_login import login_required, current_user

item = Blueprint('item', __name__)

# Upload item
@item.route("/upload", methods=["GET", "POST"])
@login_required
def upload_item():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = float(request.form.get("price") or 0)
        trade_option = request.form.get("trade_option") or "No"
        seller_id = current_user.id

        image_file = request.files.get("image")
        filename = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, "static", "uploads")
            os.makedirs(upload_path, exist_ok=True)  # make sure folder exists
            image_file.save(os.path.join(upload_path, filename))

        new_item = Item(
            title=title,
            description=description,
            price=price,
            trade_option=trade_option,
            image_path=f"uploads/{filename}" if filename else None,
            seller_id=seller_id
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("upload.html")

# Item detail
@item.route("/item/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("item_detail.html", item=item)

# Edit item
@item.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == "POST":
        item.title = request.form.get("title") or item.title
        item.description = request.form.get("description") or item.description
        try:
            item.price = float(request.form.get("price") or 0)
        except ValueError:
            pass
        item.trade_option = request.form.get("trade_option") or item.trade_option

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, "static", "uploads")
            os.makedirs(upload_path, exist_ok=True)
            image_file.save(os.path.join(upload_path, filename))
            item.image_path = f"uploads/{filename}"

        db.session.commit()
        return redirect(url_for("item.item_detail", item_id=item.id))

    return render_template("edit_item.html", item=item)

# Delete item
@item.route("/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.image_path:
        try:
            img_path = os.path.join(current_app.root_path, "static", item.image_path)
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("main.index"))