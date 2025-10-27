from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest
from .models import db, User, Category, Record
from .schemas import UserSchema, CategorySchema, RecordSchema

bp = Blueprint("api", __name__)

user_schema = UserSchema()
category_schema = CategorySchema()
record_schema = RecordSchema()

@bp.errorhandler(IntegrityError)
def handle_integrity_error(err):
    db.session.rollback()
    return jsonify({"error": "Database integrity error", "message": str(err.orig)}), 400

@bp.errorhandler(NotFound)
def handle_not_found(err):
    return jsonify({"error": "Resource not found"}), 404

@bp.errorhandler(BadRequest)
def handle_bad_request(err):
    return jsonify({"error": "Bad request", "message": str(err)}), 400

@bp.errorhandler(Exception)
def handle_general_error(err):
    db.session.rollback()
    return jsonify({"error": "Internal server error", "message": str(err)}), 500


@bp.route("/user", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "messages": errors}), 400
    user = User(name=data["name"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@bp.route("/user", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True))

@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))

@bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if "name" in data:
        user.name = data["name"]
    db.session.commit()
    return jsonify(user_schema.dump(user))

@bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

@bp.route("/category", methods=["POST"])
def create_category():
    data = request.get_json() or {}
    errors = category_schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "messages": errors}), 400

    user = User.query.get(data.get("user_id"))
    if not user:
        return jsonify({"error": "User not found"}), 404

    category = Category(name=data["name"], user_id=user.id)
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201

@bp.route("/category", methods=["GET"])
def get_categories():
    user_id = request.args.get("user_id", type=int)
    query = Category.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    categories = query.all()
    return jsonify(category_schema.dump(categories, many=True))


@bp.route("/category/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    if "name" in data:
        category.name = data["name"]
    db.session.commit()
    return jsonify(category_schema.dump(category))

@bp.route("/category/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"})


@bp.route("/record", methods=["POST"])
def create_record():
    data = request.get_json() or {}
    errors = record_schema.validate(data)
    if errors:
        return jsonify({"error": "Validation error", "messages": errors}), 400

    user = User.query.get(data["user_id"])
    category = Category.query.get(data["category_id"])
    if not user or not category:
        return jsonify({"error": "User or Category not found"}), 404
    if data["amount"] <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    record = Record(
        user_id=data["user_id"],
        category_id=data["category_id"],
        amount=data["amount"]
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record_schema.dump(record)), 201

@bp.route("/record", methods=["GET"])
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    query = Record.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)

    records = query.all()
    return jsonify(record_schema.dump(records, many=True))

@bp.route("/record/<int:record_id>", methods=["PUT"])
def update_record(record_id):
    record = Record.query.get_or_404(record_id)
    data = request.get_json()
    if "user_id" in data:
        record.user_id = data["user_id"]
    if "category_id" in data:
        record.category_id = data["category_id"]
    if "amount" in data:
        if data["amount"] <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
        record.amount = data["amount"]
    db.session.commit()
    return jsonify(record_schema.dump(record))

@bp.route("/record/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = Record.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted"})
