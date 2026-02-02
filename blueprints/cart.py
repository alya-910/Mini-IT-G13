from datetime import datetime
from flask import Blueprint, redirect, url_for, render_template, session
from models.items import Item
from flask_login import login_required

cart = Blueprint('cart', __name__)

# Add to cart
@cart.route("/add_to_cart/<int:item_id>")
@login_required
def add_to_cart(item_id):
    cart = session.get("cart", {})
    item_id_str = str(item_id)

    # Only add if not already in wishlist
    if item_id_str not in cart:
        cart[item_id_str] = 1

    session["cart"] = cart
    return redirect(url_for("item.item_detail", item_id=item_id))

# View cart
@cart.route("/cart")
@login_required
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

# Remove from cart
@cart.route("/remove_from_cart/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    cart = session.get("cart", {})
    item_id_str = str(item_id)

    if item_id_str in cart:
        del cart[item_id_str]

    session["cart"] = cart
    return redirect(url_for("cart.view_cart"))