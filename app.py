from flask import Flask, request, jsonify
import datetime
import data
import os

app = Flask(__name__)


@app.route("/user", methods=["POST"])
def create_user():
    """Add user"""
    global data
    user_data = request.get_json()
    user_id = data.user_id_counter
    data.users[user_id] = {
        "id": user_id,
        "name": user_data.get("name")
    }
    data.user_id_counter += 1
    return jsonify(data.users[user_id]), 201

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID"""
    user = data.users.get(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete user by ID"""
    if user_id in data.users:
        del data.users[user_id]
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["GET"])
def get_all_users():
    """All participants"""
    return jsonify(list(data.users.values()))


@app.route("/category", methods=["POST"])
def create_category():
    """Add category"""
    global data
    category_data = request.get_json()
    category_id = data.category_id_counter
    data.categories[category_id] = {
        "id": category_id,
        "name": category_data.get("name")
    }
    data.category_id_counter += 1
    return jsonify(data.categories[category_id]), 201

@app.route("/category", methods=["GET"])
def get_all_categories():
    """All categories"""
    return jsonify(list(data.categories.values()))

@app.route("/category", methods=["DELETE"])
def delete_category():
    """Delete category by ID"""
    category_id = request.args.get("id", type=int)
    if not category_id or category_id not in data.categories:
        return jsonify({"error": "Category not found"}), 404
    del data.categories[category_id]
    return jsonify({"message": "Category deleted"})

@app.route("/record", methods=["POST"])
def create_record():
    record_data = request.get_json()
    record_id = data.record_id_counter
    user_id = record_data.get("user_id")
    category_id = record_data.get("category_id")
    amount = record_data.get("amount")

    if user_id not in data.users or category_id not in data.categories:
        return jsonify({"error": "Invalid user or category ID"}), 400
    data.records[record_id] = {
        "id": record_id,
        "user_id": user_id,
        "category_id": category_id,
        "create_date": datetime.datetime.now().isoformat(),
        "amount": amount,
    }
    data.record_id_counter += 1 
    return jsonify(data.records[record_id]), 201

@app.route("/record/<int:record_id>", methods=["GET"])
def get_record(record_id):
    record = data.records.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(record)

@app.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    if record_id in data.records:
        del data.records[record_id]
        return jsonify({"message": "Record deleted"})
    return jsonify({"error": "Record not found"}), 404

@app.route("/record", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return jsonify({"error": "Parameters user_id or category_id required"}), 400

    filtered = [
        r for r in data.records.values()
        if (user_id is None or r["user_id"] == user_id)
        and (category_id is None or r["category_id"] == category_id)
    ]

    return jsonify(filtered)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)