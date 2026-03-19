from flask import Blueprint, jsonify
from db import get_connection

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/checkout", methods=["POST"])
def checkout():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT SUM(P.PRICE_PKR * C.QUANTITY)
    FROM CART C
    JOIN PRODUCT P
    ON C.PRODUCT_ID = P.PRODUCT_ID
    WHERE C.STATUS='active'
    """

    cursor.execute(query)

    total = cursor.fetchone()[0]

    insert_query = """
    INSERT INTO ORDERS
    (ORDER_ID, ORDER_DATE, TOTAL_AMOUNT, PAYMENT_STATUS, ORDER_STATUS)
    VALUES (ORDER_SEQ.NEXTVAL, SYSDATE, :total, 'COD', 'Processing')
    """

    cursor.execute(insert_query, {"total": total})

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order placed", "total": total})