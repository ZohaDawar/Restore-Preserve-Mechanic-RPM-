from flask import Blueprint, jsonify, request
from db import get_connection

orders_bp = Blueprint("orders", __name__)

# ✅ STEP 1: Get total only
@orders_bp.route("/checkout", methods=["GET"])
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

    cursor.close()
    conn.close()

    return jsonify({"total": total})


# ✅ STEP 2: Confirm order after payment
@orders_bp.route("/confirm-order", methods=["POST"])
def confirm_order():

    data = request.json

    total = data["total"]
    payment_method = data["method"]
    payment_status = data["status"]
    payment_id = data["payment_id"]

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO ORDERS
    (ORDER_ID, ORDER_DATE, TOTAL_AMOUNT, PAYMENT_METHOD, PAYMENT_STATUS, PAYMENT_ID, ORDER_STATUS)
    VALUES
    (ORDER_SEQ.NEXTVAL, SYSDATE, :total, :method, :status, :pid, 'Processing')
    """

    cursor.execute(insert_query, {
        "total": total,
        "method": payment_method,
        "status": payment_status,
        "pid": payment_id
    })

    # ✅ Clear cart after order
    cursor.execute("UPDATE CART SET STATUS='checked_out' WHERE STATUS='active'")

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order confirmed successfully"})
