import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


### Create the Flask app ###

app = Flask(__name__)

### SQLite database ###

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.root_path, "thrift.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

### Models ###

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    trade_option = db.Column(db.String(10))
    image_path = db.Column(db.String(200))
    seller_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))


### Routes ###

@app.route("/")
def index():
    items = Item.query.all()
    return render_template("index.html", items=items)

@app.route("/upload", methods=["GET", "POST"])
def upload_item():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = float(request.form.get("price") or 0)
        trade = request.form.get("trade_option") or "No"

        image_file = request.files.get("image")
        filename = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join("static", "uploads", filename))

        new_item = Item(
            title=title,
            description=description,
            price=price,
            trade_option=trade,
            image_path=f"uploads/{filename}" if filename else None
        )

        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("upload.html")


### Item detail / Edit / Delete routes ###

from flask import abort  # add at top of file if not already imported

@app.route("/item/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("item_detail.html", item=item)

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == "POST":
        item.title = request.form.get("title") or item.title
        item.description = request.form.get("description") or item.description
        try:
            item.price = float(request.form.get("price") or 0)
        except ValueError:
            item.price = item.price or 0.0
        item.trade_option = request.form.get("trade_option") or item.trade_option

        file = request.files.get("image")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, "static", "uploads", filename))
            item.image_path = f"uploads/{filename}"

        db.session.commit()
        return redirect(url_for("item_detail", item_id=item.id))

    return render_template("edit_item.html", item=item)

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    # optional: remove image file from disk (not required)
    if item.image_path:
        try:
            img_path = os.path.join(app.root_path, "static", item.image_path)
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

### Run app and create database ###

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route("/item/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("item_detail.html", item=item)

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == "POST":
        item.title = request.form.get("title")
        item.description = request.form.get("description")
        item.price = float(request.form.get("price") or 0)
        item.trade_option = request.form.get("trade_option")

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join("static", "uploads", filename))
            item.image_path = f"uploads/{filename}"

        db.session.commit()
        return redirect(url_for("item_detail", item_id=item.id))

    return render_template("edit_item.html", item=item)

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))

