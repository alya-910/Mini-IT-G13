import os
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ------------------------------
# 1 Create Flask app
# ------------------------------
app = Flask(__name__)
app.secret_key = "cart-secret-key"  # Needed for session (cart)

# ------------------------------
# 2 Configure database
# ------------------------------
db_path = os.path.join(app.root_path, "thrift.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------------------
# 3️ Define Models
# ------------------------------

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    trade_option = db.Column(db.String(10))
    image_path = db.Column(db.String(200))
    seller_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

# Optional CartItem model if storing in database (here we use session)
# class CartItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

# ------------------------------
# 4 Routes
# ------------------------------

# Homepage / Marketplace
@app.route('/')
def index():
    items = Item.query.all()
    return render_template("index.html", items=items)

# Upload item
@app.route("/upload", methods=["GET", "POST"])
def upload_item():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = float(request.form.get("price") or 0)
        trade_option = request.form.get("trade_option") or "No"

        image_file = request.files.get("image")
        filename = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(app.root_path, "static", "uploads")
            os.makedirs(upload_path, exist_ok=True)  # make sure folder exists
            image_file.save(os.path.join(upload_path, filename))

        new_item = Item(
            title=title,
            description=description,
            price=price,
            trade_option=trade_option,
            image_path=f"uploads/{filename}" if filename else None
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("upload.html")

# Item detail
@app.route("/item/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template("item_detail.html", item=item)

# Edit item
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
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
            upload_path = os.path.join(app.root_path, "static", "uploads")
            os.makedirs(upload_path, exist_ok=True)
            image_file.save(os.path.join(upload_path, filename))
            item.image_path = f"uploads/{filename}"

        db.session.commit()
        return redirect(url_for("item_detail", item_id=item.id))

    return render_template("edit_item.html", item=item)

# Delete item
@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
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

# Add to cart
@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    cart = session.get("cart", {})  # get existing cart or empty
    item_id_str = str(item_id)
    if item_id_str in cart:
        cart[item_id_str] += 1
    else:
        cart[item_id_str] = 1
    session["cart"] = cart
    return redirect(url_for("item_detail", item_id=item_id))

# View cart
@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    for item_id_str, qty in cart.items():
        item = Item.query.get(int(item_id_str))
        if item:
            items.append((item, qty))
            total += (item.price or 0) * qty
    return render_template("cart.html", items=items, total=total)

# Checkout
@app.route("/checkout", methods=["POST"])
def checkout():
    session.pop("cart", None)  # clear cart
    return render_template("checkout.html")

# Remove from cart
@app.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    cart = session.get("cart", {})
    item_id_str = str(item_id)

    if item_id_str in cart:
        del cart[item_id_str]

    session["cart"] = cart
    return redirect(url_for("view_cart"))

# ------------------------------
# 5 Run app and create database
# ------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables if not exist
    app.run(debug=True)