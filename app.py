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



if __name__ == "__main__":
    app.run(debug=True)