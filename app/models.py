from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash

from app.extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    price_cents = db.Column(db.Integer)
    picture_url = db.Column(db.Text)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship("User", uselist=False, back_populates="products")

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship("Store", uselist=False, back_populates="products")

    db.Index('idx_name_and_desc', 'name', 'description')

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError('needs to have a name')
        return name


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    store = db.relationship("Store", uselist=False, back_populates='user')
    products = db.relationship("Product", back_populates='creator')

    @classmethod
    def create(cls, email, password):
        if not email or not password:
            raise ValueError('email and password are required')
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", uselist=False, back_populates="store")

    products = db.relationship("Product", back_populates='store')

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError('needs to have a name')
        return name



