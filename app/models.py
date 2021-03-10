from sqlalchemy.orm import validates

from app.extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    db.Index('idx_name_and_desc', 'name', 'description')

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError('needs to have a name')
        return name

