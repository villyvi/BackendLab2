from flask import Flask, request, jsonify
import datetime
import data

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


if __name__ == "__main__":
    app.run(debug=True)