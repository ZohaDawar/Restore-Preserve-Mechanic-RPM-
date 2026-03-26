from flask import Blueprint, jsonify, request
from db import get_connection

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/", methods=["GET"])
def view_cart():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT P.PRODUCT_NAME, C.QUANTITY, P.PRICE_PKR
    FROM CART C
    JOIN PRODUCT P
    ON C.PRODUCT_ID = P.PRODUCT_ID
    WHERE C.STATUS='active'
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


@cart_bp.route("/add", methods=["POST"])
def add_to_cart():

    data = request.json
    product_id = data["product_id"]
    quantity = data["quantity"]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO CART (CART_ID, PRODUCT_ID, QUANTITY, ADDED_DATE, STATUS)
    VALUES (CART_SEQ.NEXTVAL, :pid, :qty, SYSDATE, 'active')
    """

    cursor.execute(query, {"pid": product_id, "qty": quantity})

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Product added to cart"})
