from flask import Flask
from flask_cors import CORS

from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp

app = Flask(__name__)
CORS(app)

# ✅ Home route (fixes 404 on "/")
@app.route('/')
def home():
    return "Backend is running"

# ✅ Blueprints
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(orders_bp, url_prefix="/orders")

if __name__ == "__main__":
    app.run(debug=True)
