from flask import Flask, render_template, request, session, redirect, url_for
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret"

MENU_ITEMS = [
    {
        "id": 1,
        "name": "Margherita Pizza",
        "description": "Fresh mozzarella, basil, tomato sauce.",
        "price": 9.99,
        "image": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 2,
        "name": "BBQ Chicken Burger",
        "description": "Smoky sauce, crispy onions, melt cheddar.",
        "price": 11.99,
        "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 3,
        "name": "Caesar Salad",
        "description": "Romaine, parmesan, crunchy croutons.",
        "price": 8.49,
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 4,
        "name": "Sushi Platter",
        "description": "Assorted rolls, fresh sashimi, soy dip.",
        "price": 16.99,
        "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 5,
        "name": "Pasta Alfredo",
        "description": "Creamy garlic sauce, parmesan, parsley.",
        "price": 12.49,
        "image": "https://images.unsplash.com/photo-1521389508051-d7ffb5dc8d9d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "id": 6,
        "name": "Chocolate Brownie",
        "description": "Warm, fudgy, with vanilla ice cream.",
        "price": 5.99,
        "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=800&q=80"
    }
]


def get_cart():
    cart = session.get("cart")
    if cart is None:
        cart = {}
        session["cart"] = cart
    return cart


def get_item(item_id):
    return next((item for item in MENU_ITEMS if item["id"] == item_id), None)


def compute_cart_totals(cart):
    items = []
    total = Decimal("0.00")

    for item_id_str, quantity in cart.items():
        item_id = int(item_id_str)
        menu_item = get_item(item_id)
        if not menu_item:
            continue
        subtotal = Decimal(str(menu_item["price"])) * quantity
        total += subtotal
        items.append({
            "id": item_id,
            "name": menu_item["name"],
            "price": menu_item["price"],
            "quantity": quantity,
            "subtotal": float(subtotal),
            "image": menu_item["image"]
        })

    return items, float(total)


@app.route("/")
def index():
    cart = get_cart()
    cart_count = sum(cart.values())
    return render_template("index.html", menu=MENU_ITEMS, cart_count=cart_count)


@app.route("/cart")
def cart_page():
    cart = get_cart()
    items, total = compute_cart_totals(cart)
    return render_template("cart.html", items=items, total=total)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    data = request.get_json() or {}
    item_id = int(data.get("item_id", 0))
    item = get_item(item_id)
    if not item:
        return {"success": False, "message": "Item not found"}, 404

    cart = get_cart()
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    session["cart"] = cart
    cart_count = sum(cart.values())
    return {"success": True, "cart_count": cart_count}


@app.route("/update_cart", methods=["POST"])
def update_cart():
    cart = get_cart()
    for key, value in request.form.items():
        if key.startswith("quantity_"):
            item_id = key.split("quantity_")[1]
            try:
                quantity = int(value)
            except ValueError:
                quantity = 1
            if quantity <= 0:
                cart.pop(item_id, None)
            else:
                cart[item_id] = quantity

    session["cart"] = cart
    return redirect(url_for("cart_page"))


@app.route("/checkout", methods=["POST"])
def checkout():
    customer_name = request.form.get("customer_name", "Guest")
    customer_address = request.form.get("customer_address", "")
    contact_phone = request.form.get("contact_phone", "")

    cart = get_cart()
    items, total = compute_cart_totals(cart)
    if not items:
        return redirect(url_for("cart_page"))

    order = {
        "customer_name": customer_name,
        "customer_address": customer_address,
        "contact_phone": contact_phone,
        "items": items,
        "total": total,
        "order_number": "FT" + str(1000 + len(cart))
    }

    session.pop("cart", None)
    return render_template("confirmation.html", order=order)


if __name__ == "__main__":
    app.run(debug=True)
