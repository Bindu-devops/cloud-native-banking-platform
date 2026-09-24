from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)

accounts = [
    {
        "account_id": "10001",
        "name": "John Doe",
        "balance": 10000.0
    },
    {
        "account_id": "10002",
        "name": "Jane Smith",
        "balance": 15000.0
    }
]

transactions = []


@app.route("/")
def home():
    return jsonify({
        "application": "Cloud-Native Banking Platform",
        "version": "1.0.0",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/accounts", methods=["GET"])
def get_accounts():
    return jsonify(accounts)


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "error": "Account name is required"
        }), 400

    account = {
        "account_id": str(10000 + len(accounts) + 1),
        "name": data["name"],
        "balance": 0.0
    }

    accounts.append(account)

    return jsonify(account), 201


@app.route("/accounts/<account_id>", methods=["GET"])
def get_account(account_id):
    account = next(
        (
            account
            for account in accounts
            if account["account_id"] == account_id
        ),
        None
    )

    if not account:
        return jsonify({
            "error": "Account not found"
        }), 404

    return jsonify(account)


@app.route("/transactions", methods=["POST"])
def create_transaction():
    data = request.get_json()

    required_fields = [
        "from_account",
        "to_account",
        "amount"
    ]

    if not data or not all(
        field in data for field in required_fields
    ):
        return jsonify({
            "error": "from_account, to_account and amount are required"
        }), 400

    if data["amount"] <= 0:
        return jsonify({
            "error": "Transaction amount must be greater than zero"
        }), 400

    transaction = {
        "transaction_id": str(uuid4()),
        "from_account": data["from_account"],
        "to_account": data["to_account"],
        "amount": data["amount"],
        "status": "SUCCESS"
    }

    transactions.append(transaction)

    return jsonify(transaction), 201


@app.route("/transactions/<transaction_id>")
def get_transaction(transaction_id):
    transaction = next(
        (
            transaction
            for transaction in transactions
            if transaction["transaction_id"] == transaction_id
        ),
        None
    )

    if not transaction:
        return jsonify({
            "error": "Transaction not found"
        }), 404

    return jsonify(transaction)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)