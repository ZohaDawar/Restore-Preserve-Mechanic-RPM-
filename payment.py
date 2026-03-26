from flask import Blueprint, request, jsonify
import random

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/simulate", methods=["POST"])
def simulate_payment():

    data = request.json
    amount = data.get("amount")

    return jsonify({
        "status": "success",
        "payment_id": "TEST_" + str(random.randint(1000, 9999)),
        "amount": amount
    })
