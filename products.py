from flask import Blueprint, jsonify, request
from db import get_connection

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["GET"])
def get_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM PRODUCT")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


@products_bp.route("/search/<name>", methods=["GET"])
def search_product(name):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM PRODUCT
    WHERE UPPER(PRODUCT_NAME) LIKE '%' || :name || '%'
    """

    cursor.execute(query, {"name": name.upper()})

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)
