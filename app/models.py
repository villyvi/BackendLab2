from . import db
from sqlalchemy.sql import func

class Record(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False, unique=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    amount = db.Column(db.Float(precision=2), nullable=False)

    user = db.relationship("User", back_populates="records")
    category = db.relationship("Category", back_populates="records")


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    records = db.relationship("Record", back_populates="user", cascade="all, delete-orphan")
    categories = db.relationship("Category", back_populates="user", cascade="all, delete-orphan")


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=False)

    records = db.relationship("Record", back_populates="category", cascade="all, delete-orphan")
    user = db.relationship("User", back_populates="categories")
