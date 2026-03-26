from flask import Flask
from flask_cors import CORS

from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from routes.payment import payment_bp   # ✅ NEW

app = Flask(__name__)
CORS(app)

# Register all routes
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(payment_bp, url_prefix="/payment")  # ✅ NEW

if __name__ == "__main__":
    app.run(debug=True)
