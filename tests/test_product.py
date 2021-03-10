from app import db
from app.models import Product


def test_product_creation(client, init_database):
    assert Product.query.count() == 0
    book = Product(name="Sherlock Homes", description="a house hunting detective")
    db.session.add(book)
    db.session.commit()
    assert Product.query.count() == 1
    assert Product.query.first().name == book.name

